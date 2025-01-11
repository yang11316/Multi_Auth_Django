from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.conf import settings
from commonutils import utils
from commonutils import accumulator
from commonutils import kgc
from commonutils import switch_interface
from commonutils import PKI
from .models import *
from usermanage.models import UserTable
from softwaremanage.models import SoftwareTable
from nodemanage.models import NodeTable
from domainmanage.models import DomainTable
from ddsmanage.models import DDSInfoTable, PacketID

import json, datetime, os
from fastecdsa import keys
import requests
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy
import time


# Create your views here.

# 加载PKI证书
self_cert = PKI.load_cert_from_pem_file(settings.AS_CRT)
ca_cert = PKI.load_cert_from_pem_file(settings.CA_CRT)
self_private_key = PKI.load_key_from_pem_file(settings.AS_KEY)

acc = accumulator.Accumulator()
kgc = kgc.KGC()
# if os.path.exists("accumulator.json"):
#     acc.setup_from_file("accumulator.json")
# get calculated pids
temp_params = KGCParamterTable.objects.get(kgc_id="kgc_id")
acc.public_key = utils.hex2int(temp_params.kgc_acc_publickey)
acc.G = utils.hex2int(temp_params.kgc_acc_G)
acc.serect_key = (
    utils.hex2int(temp_params.kgc_acc_serectkey0),
    utils.hex2int(temp_params.kgc_acc_serectkey1),
)
acc.acc_cur = utils.hex2int(temp_params.kgc_acc_cur)
kgc.s = utils.hex2int(temp_params.kgc_s)
kgc.Ppub = keys.get_public_key(kgc.s, kgc.ec_curve)


temp_pids = EnityTable.objects.filter(entity_parcialkey__isnull=False)
for temp in temp_pids:
    acc.pids.append(temp.entity_pid)
print(acc.pids)


# kgc初始化
def kgc_paramter_init(request):
    if request.method == "POST":
        try:
            kgc.set_up()
            acc.setup()
            kgc_instance = KGCParamterTable.objects.filter(kgc_id="kgc_id")
            kgc_instance.kgc_s = kgc.get_s()
            kgc_instance.kgc_Ppub = kgc.get_Ppub()
            kgc_instance.kgc_q = kgc.get_q()
            kgc_instance.kgc_acc_G = acc.get_G()
            kgc_instance.kgc_acc_publickey = acc.get_publickey()
            kgc_instance.kgc_acc_cur = acc.get_acc_cur()
            kgc_instance.kgc_acc_serectkey0 = acc.get_serect_key_0()
            kgc_instance.kgc_acc_serectkey1 = acc.get_serect_key_1()
            kgc_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def kgc_paramter_save():
    kgc_instance = KGCParamterTable.objects.get(kgc_id="kgc_id")
    kgc_instance.kgc_s = kgc.get_s()
    kgc_instance.kgc_Ppub = kgc.get_Ppub()
    kgc_instance.kgc_q = kgc.get_q()
    kgc_instance.kgc_acc_G = acc.get_G()
    kgc_instance.kgc_acc_publickey = acc.get_publickey()
    kgc_instance.kgc_acc_cur = acc.get_acc_cur()
    kgc_instance.kgc_acc_serectkey0 = acc.get_serect_key_0()
    kgc_instance.kgc_acc_serectkey1 = acc.get_serect_key_1()
    kgc_instance.save()


def entity_query_alive_by_uid(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            query_instance = EnityTable.objects.filter(
                is_alive=True, user_id=json_data["user_id"]
            )
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def entity_query_alive(request):
    """
    return alive nodes
    """
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = EnityTable.objects.filter(is_alive=True)
            length = query_instance.count()
            if length < page * limit:
                send_instance = query_instance[(page - 1) * limit : length]
            else:
                send_instance = query_instance[(page - 1) * limit : page * limit]
            data = {
                # "num": send_instance.count(),
                "num": length,
                "data": [temp.get_data() for temp in send_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 测试使用
@csrf_exempt
def entity_add(request):
    """
    add entity
    """
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            entity_instance = EnityTable()
            user_instance = UserTable.objects.get(user_id=json_data["user_id"])
            software_instance = SoftwareTable.objects.get(
                software_id=json_data["software_id"]
            )
            node_instance = NodeTable.objects.get(node_id=json_data["node_id"])
            node_ip = node_instance.node_ip
            node_port = node_instance.node_port
            sowftware_hash = software_instance.software_hash
            entity_ip = json_data["entity_ip"]

            # 重复检测，每次pid都是随机生成，一个entity_ip可能会重复部署程序，可以查询entity_ip和software_id来解决
            if (
                EnityTable.objects.filter(
                    entity_ip=entity_ip, software_id=software_instance
                ).count()
                != 0
            ):
                return JsonResponse(
                    {"status": "error", "message": "entity_ip and software_id is exist"}
                )

            entity_instance.entity_pid = utils.calculate_pid(sowftware_hash, entity_ip)
            entity_instance.software_id = software_instance
            entity_instance.software_name = software_instance.software_name
            entity_instance.node_id = node_instance
            entity_instance.user_id = user_instance
            entity_instance.entity_ip = entity_ip
            entity_instance.create_time = datetime.datetime.now()
            entity_instance.update_time = datetime.datetime.now()
            # 发送对应的ap，如果部署ap围在线就退出
            payload = {
                "add_data": {
                    "entity_pid": entity_instance.entity_pid,
                    "software_id": json_data["software_id"],
                    "software_hash": software_instance.software_hash,
                    "user_id": json_data["user_id"],
                    "entity_ip": entity_ip,
                }
            }
            response = post_to_ap(
                node_ip,
                node_port,
                "/entitymanage/addentity/",
                payload=payload,
            )
            # print(response.json())
            if response.json()["status"] == "success":
                entity_instance.save()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse(
                    {"status": "error", "message": response.json()["message"]}
                )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def entity_query_pid(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("query_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            entity_pid = json_data["entity_pid"]
            query_instance = EnityTable.objects.get(entity_pid=entity_pid)
            data = query_instance.get_data()
            return JsonResponse({"status": "success", "message": data})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def entity_query_all(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = EnityTable.objects.all()
            length = query_instance.count()
            if length < page * limit:
                send_instance = query_instance[(page - 1) * limit : length]
            else:
                send_instance = query_instance[(page - 1) * limit : page * limit]

            data = {
                # "num": send_instance.count(),
                "num": length,
                "data": [temp.get_data() for temp in send_instance],
            }

            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 计算实体的部分私钥
def entity_calculate_parcialkey(request):
    if request.method == "POST":
        # 深拷贝一份acc，以便还原
        global acc
        # print(acc.pids)
        tmp_acc = deepcopy(acc)
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            entity_pid = json_data["entity_pid"]
            count = int(json_data["count"])
            # print(entity_pid)
            # 判断json——data是否存在于数据库中，如果都存在就执行，否则返回错误
            if not EnityTable.objects.filter(entity_pid=entity_pid).exists():
                return JsonResponse(
                    {"status": "error", "message": "entity_pid is not exist"}
                )
            # 判断节点是否已经下发过密钥
            entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
            # 判断要下发的节点是否存活
            if not entity_instance.node_id.node_is_alive:
                return JsonResponse({"status": "error", "message": "node is not alive"})
            if entity_instance.entity_parcialkey != None:
                return JsonResponse(
                    {"status": "error", "message": "entity_parcialkey is exist"}
                )

            # print("build start")
            # 批量建立pid 未save
            entity_instance_list = [entity_instance]
            for i in range(1, count):
                tmp_instance = EnityTable()
                tmp_instance.entity_pid = utils.calculate_pid(
                    entity_instance.software_id.software_hash, entity_instance.entity_ip
                )
                tmp_instance.software_id = entity_instance.software_id
                tmp_instance.software_name = entity_instance.software_name
                tmp_instance.node_id = entity_instance.node_id
                tmp_instance.user_id = entity_instance.user_id
                tmp_instance.entity_ip = entity_instance.entity_ip
                entity_instance_list.append(tmp_instance)
            # print("calculate start")
            # 计算parcialkey
            entity_pair = []
            aux = ""
            if len(acc.pids) == 0:
                # 系统内没有计算的证据值
                for tmp_instance in entity_instance_list:
                    acc.add_member(tmp_instance.entity_pid)
                for tmp_instance in entity_instance_list:
                    tmp_instance.entity_parcialkey = acc.witness_generate_by_pid(
                        tmp_instance.entity_pid
                    )
                    entity_pair.append(
                        {
                            "entity_pid": tmp_instance.entity_pid,
                            "entity_parcialkey": tmp_instance.entity_parcialkey,
                        }
                    )
            else:
                update_pid = []
                for tmp_instance in entity_instance_list:
                    if tmp_instance.entity_pid in acc.pids:
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "entity_pid is already exist",
                            }
                        )
                    acc.add_member(tmp_instance.entity_pid)
                    update_pid.append(tmp_instance.entity_pid)
                for tmp_instance in entity_instance_list:
                    tmp_instance.entity_parcialkey = acc.witness_generate_by_pid(
                        tmp_instance.entity_pid
                    )
                    entity_pair.append(
                        {
                            "entity_pid": tmp_instance.entity_pid,
                            "entity_parcialkey": tmp_instance.entity_parcialkey,
                        }
                    )
                # 计算更新凭证
                aux = acc.get_new_aux(update_pid)
                # 更新本地的部分私钥
                entity_parcialkey_instance = EnityTable.objects.filter(
                    entity_parcialkey__isnull=False
                )
                for tmp_instance in entity_parcialkey_instance:
                    tmp_instance.entity_parcialkey = acc.update_witness(
                        aux, tmp_instance.entity_parcialkey
                    )
                    tmp_instance.save()
                print("aux:", aux)
            # 向对应ap发送entity信息,发送成功则save
            post_data = {
                "software_id": entity_instance.software_id.software_id,
                "user_id": entity_instance.user_id.user_id,
                "entity_ip": entity_instance.entity_ip,
                "software_hash": entity_instance.software_id.software_hash,
                "acc_cur": utils.int2hex(acc.acc_cur),
                "entity_pair": entity_pair,
                "aux": aux,
            }
            print(post_data)
            node_ip = entity_instance.node_id.node_ip
            node_port = entity_instance.node_id.node_port
            response = post_to_ap(
                node_ip,
                node_port,
                "/entitymanage/getentity/",
                payload=post_data,
            )
            print(response)
            if response.json()["status"] != "success":
                # 还原acc
                acc = deepcopy(tmp_acc)
                return JsonResponse(
                    {"status": "error", "message": response.json()["message"]}
                )
            else:
                for tmp_entity in entity_instance_list:
                    tmp_entity.save()
                    kgc_paramter_save()
            # 如果aux不为空 向其他ap发送更新凭证
            if aux != "":
                post_data = {
                    "aux_data": {
                        "aux": aux,
                        "acc_cur": utils.int2hex(acc.acc_cur),
                    }
                }
                node_instance_all = NodeTable.objects.filter(node_is_alive=True)
                for node_instance in node_instance_all:
                    if node_instance.node_id != entity_instance.node_id.node_id:
                        response = post_to_ap(
                            node_instance.node_ip,
                            node_instance.node_port,
                            "/entitymanage/getauxdata/",
                            payload=post_data,
                        )
                        if response == None:
                            print(
                                "can not send aux to node:",
                                node_instance.node_id,
                                ", node is not alive",
                            )
            return JsonResponse({"status": "success"})

        except Exception as e:
            acc = deepcopy(tmp_acc)
            return JsonResponse({"status": "error", "message": str(e)})


# 撤销实体
@csrf_exempt
def entity_withdraw(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            entity_pid = json_data.get("entity_pid")
            entity_instance = EnityTable.objects.filter(entity_pid=entity_pid).exists()
            if not entity_instance:
                return JsonResponse({"status": "error", "message": "pid not exists"})
            entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
            if entity_instance.entity_parcialkey == None:
                return JsonResponse(
                    {"status": "error", "message": "entity doesn't have parcialkey"}
                )
            # 生成aux
            aux = acc.remove_member(entity_pid)
            node_instance_all = NodeTable.objects.filter(node_is_alive=True)
            payload = {
                "aux_data": {
                    "aux": aux,
                    "acc_cur": utils.int2hex(acc.acc_cur),
                    "withdraw_pid": entity_pid,
                }
            }
            # 发送更新凭证
            for tmp_node in node_instance_all:
                node_ip = tmp_node.node_ip
                node_port = tmp_node.node_port
                response = post_to_ap(
                    node_ip,
                    node_port,
                    "/entitymanage/getauxdata/",
                    payload=payload,
                )
                if response == None:
                    print(
                        "can not send aux to node:",
                        tmp_node.node_ip,
                        ", node is not alive",
                    )
                    tmp_node.node_is_alive = False
                    tmp_node.save()
                    continue
                if response.json()["status"] != "success":
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": response.json()["message"],
                        }
                    )
            # 更新AS上的部分私钥记录
            temp_pids = EnityTable.objects.filter(entity_parcialkey__isnull=False)
            for tmp in temp_pids:
                tmp.entity_parcialkey = acc.update_witness(aux, tmp.entity_parcialkey)
                tmp.save()
            entity_instance.delete()
            kgc_paramter_save()

            # 组成rfac报文并发送
            # dds type指定信息的类型
            # 1、publisher 1:向组ip发送消息
            # 2、subscriber 2:接收组ip的消息

            # protocol type指定信息的传输协议
            # 1、tcp :1
            # 2、udp :2
            if DDSInfoTable.objects.filter(entity_pid=entity_pid).exists():
                dds_instance = DDSInfoTable.objects.filter(entity_pid=entity_pid)
                for ddsinstance in dds_instance:
                    dds_type = ddsinstance.dds_type
                    protocol_type = ddsinstance.protocol_type
                    # 生成RFAC包，默认code为2，表示deny
                    rfac_packet = switch_interface.RFACPacket(
                        2, PacketID.get_next_id(), 1
                    )
                    # 根据dds_type和protocol_type设置协议
                    if dds_type == 1:
                        if protocol_type == 1:
                            rfac_packet.set_protocol(6)
                        elif protocol_type == 2:
                            rfac_packet.set_protocol(17)
                    else:
                        rfac_packet.set_protocol(2)
                    # 设置IP、端口、掩码和MAC地址
                    rfac_packet.set_ip(1, ddsinstance.source_ip)
                    rfac_packet.set_port(2, ddsinstance.source_port)
                    rfac_packet.set_mask(3, ddsinstance.source_mask)
                    rfac_packet.set_ip(4, ddsinstance.destination_ip)
                    rfac_packet.set_port(5, ddsinstance.destination_port)
                    rfac_packet.set_mask(6, ddsinstance.destination_mask)
                    rfac_packet.set_mac(8, ddsinstance.source_mac)
                    rfac_packet.set_mac(9, ddsinstance.destination_mac)
                    # 构建包数据并发送
                    pack_data = rfac_packet.build()
                    switch_interface.send_raw_packet(pack_data, settings.SWITHCH_MAC)
                    # 删除该记录
                    ddsinstance.delete()

            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


# 发送公共参数
@csrf_exempt
def send_public_parameter(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)

            # 获取节点ip，进行ip校验
            node_ip = request.META.get("REMOTE_ADDR")
            node_entity = NodeTable.objects.filter(node_ip=node_ip).exists()
            if not node_entity:
                return JsonResponse({"status": "error", "message": "node not exists"})

            # 校验AP的PKI证书是否正确
            ap_cert_str = json_data["cert"]
            ap_cert = PKI.load_cert_from_string(ap_cert_str)
            # 如果不是CA签发的证书，返回错误
            if not PKI.verify_certificate(ap_cert, ca_cert):
                node_entity = NodeTable.objects.get(node_ip=node_ip)
                node_entity.node_is_alive = False
                node_entity.save()
                return JsonResponse(
                    {"status": "error", "message": "verify PKI certificate failed"}
                )

            # 构造返回报文
            domain_id = DomainTable.objects.get(domain_ip="0.0.0.0").domain_id
            kgcinstance = KGCParamterTable.objects.get(kgc_id="kgc_id")
            data = {
                "cert": PKI.load_cert_as_string(self_cert),
                "kgc_id": "kgc_id",
                "acc_publickey": kgcinstance.kgc_acc_publickey,
                "acc_cur": kgcinstance.kgc_acc_cur,
                "kgc_q": kgcinstance.kgc_q,
                "kgc_Ppub": kgcinstance.kgc_Ppub,
                "domain_id": domain_id,
            }

            # 更新AP的存活状态
            node_entity = NodeTable.objects.get(node_ip=node_ip)
            node_entity.node_is_alive = True
            node_entity.save()

            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


# 从ap获取存活实体的pid
@csrf_exempt
def get_alive_entity_pid(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("entity_data")
            entity_pid = json_data["entity_pid"]
            entity_sending_port = json_data["entity_sending_port"]
            entity_listening_port = json_data["entity_listening_port"]
            entity_processid = json_data["entity_processid"]
            entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
            entity_instance.is_alive = True
            entity_instance.entity_listening_port = entity_listening_port
            entity_instance.entity_sending_port = entity_sending_port
            entity_instance.entity_porecessid = entity_processid
            entity_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def get_down_entity_pid(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("entity_data")
            entity_pid_list = json_data["entity_pid"]
            print(entity_pid_list)
            for entity_pid in entity_pid_list:
                entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
                entity_instance.is_alive = False
                entity_instance.entity_listening_port = 0
                entity_instance.entity_sending_port = 0
                entity_instance.entity_porecessid = ""
                entity_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


# 接收其他子课题传来的流数据
"""
{"revoke_data":
    {
        "source_ip":"xxxxxx",
        "source_port":"xxxxx",
        "source_mac":"xxxxxx",
        "destination_ip":"xxxxxx",
        "destination_port":"xxxxxx",
        "destination_mac":"xxxxxx",
        "protocol_type":"xxxxxx"
    }
}
"""


def get_revoke_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("revoke_data")
            source_ip = json_data["source_ip"]
            source_port = json_data["source_port"]
            source_mac = json_data["source_mac"]
            destination_ip = json_data["destination_ip"]
            destination_port = json_data["destination_port"]
            destination_mac = json_data["destination_mac"]
            protocol_type = json_data["protocol_type"]
            ddsinstance = DDSInfoTable.objects.filter(
                source_ip=source_ip,
                source_port=source_port,
                source_mac=source_mac,
                destination_ip=destination_ip,
                destination_port=destination_port,
                destination_mac=destination_mac,
                protocol_type=protocol_type,
            ).first()
            if not ddsinstance:
                return JsonResponse({"status": "error", "message": "not find entity"})
            entity_pid = ddsinstance.entity_pid

            """向交换机发送rfac报文 """
            # 根据entity_pid循环删除ddsinfotable中的记录，并构造rfac包发出去
            pid_records = DDSInfoTable.objects.filter(entity_pid=entity_pid)
            for pid_instance in pid_records:
                dds_type = pid_instance.dds_type
                protocol_type = pid_instance.protocol_type
                # 生成RFAC包，默认code为2，表示deny
                rfac_packet = switch_interface.RFACPacket(2, PacketID.get_next_id(), 1)
                # 根据dds_type和protocol_type设置协议
                if dds_type == 1:
                    if protocol_type == 1:
                        rfac_packet.set_protocol(6)
                    elif protocol_type == 2:
                        rfac_packet.set_protocol(17)
                else:
                    rfac_packet.set_protocol(2)
                # 设置IP、端口、掩码和MAC地址
                rfac_packet.set_ip(1, pid_instance.source_ip)
                rfac_packet.set_port(2, pid_instance.source_port)
                rfac_packet.set_mask(3, pid_instance.source_mask)
                rfac_packet.set_ip(4, pid_instance.destination_ip)
                rfac_packet.set_port(5, pid_instance.destination_port)
                rfac_packet.set_mask(6, pid_instance.destination_mask)
                rfac_packet.set_mac(8, pid_instance.source_mac)
                rfac_packet.set_mac(9, pid_instance.destination_mac)
                # 构建包数据并发送
                pack_data = rfac_packet.build()
                switch_interface.send_raw_packet(pack_data, settings.SWITHCH_MAC)
                # 删除该记录
                pid_instance.delete()

            """执行身份撤销"""
            entity_instance = EnityTable.objects.filter(entity_pid=entity_pid).exists()
            if not entity_instance:
                return JsonResponse({"status": "error", "message": "pid not exists"})
            entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
            if entity_instance.entity_parcialkey == None:
                return JsonResponse(
                    {"status": "error", "message": "entity doesn't have parcialkey"}
                )
            # 生成aux
            aux = acc.remove_member(entity_pid)
            node_instance_all = NodeTable.objects.filter(node_is_alive=True)
            payload = {
                "aux_data": {
                    "aux": aux,
                    "acc_cur": utils.int2hex(acc.acc_cur),
                    "withdraw_pid": entity_pid,
                }
            }
            # 发送更新凭证
            for tmp_node in node_instance_all:
                node_ip = tmp_node.node_ip
                node_port = tmp_node.node_port
                response = post_to_ap(
                    node_ip,
                    node_port,
                    "/entitymanage/getauxdata/",
                    payload=payload,
                )
                if response == None:
                    print(
                        "can not send aux to node:",
                        tmp_node.node_ip,
                        ", node is not alive",
                    )
                    tmp_node.node_is_alive = False
                    tmp_node.save()
                    continue
                if response.json()["status"] != "success":
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": response.json()["message"],
                        }
                    )
            # 更新AS上的部分私钥记录
            temp_pids = EnityTable.objects.filter(entity_parcialkey__isnull=False)
            for tmp in temp_pids:
                tmp.entity_parcialkey = acc.update_witness(aux, tmp.entity_parcialkey)
                tmp.save()
            entity_instance.delete()
            kgc_paramter_save()

        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


def post_to_ap(node_ip: str, node_port: int, path: str, payload: dict):
    header = {"content-type": "application/json", "Connection": "close"}
    url = "http://" + node_ip + ":" + str(node_port) + path
    data = json.dumps(payload)
    try:
        res = requests.post(url, data=data, headers=header)
        return res
    except Exception as e:
        node_instance = NodeTable.objects.get(node_ip=node_ip)
        node_instance.node_is_alive = False
        node_instance.save()
        print(e)
        return None
