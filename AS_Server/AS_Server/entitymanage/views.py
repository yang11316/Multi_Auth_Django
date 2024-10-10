from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from commonutils import utils
from commonutils import accumulator
from commonutils import kgc
from .models import *
from usermanage.models import UserTable
from softwaremanage.models import SoftwareTable
from nodemanage.models import NodeTable
import json, datetime, os
from fastecdsa import keys
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
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
                "num": send_instance.count(),
                "data": [temp.get_data() for temp in send_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 创建实体
@csrf_exempt
def entity_add(request):
    """
    add entity
    """
    if request.method == "POST":
        try:
            # json_data = request.POST.get("add_data")
            # json_data = json.loads(json_data)
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
                "num": send_instance.count(),
                "data": [temp.get_data() for temp in send_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 计算实体的部分私钥
def entity_calculate_parcialkey(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("calculate_data")
            json_data = json.loads(request.body.decode("utf-8"))
            entity_pid = json_data["entity_pid"]
            json_data = [entity_pid]
            # 判断json——data是否存在于数据库中，如果都存在于就执行，否则返回错误
            if EnityTable.objects.filter(entity_pid=entity_pid).count() == 0:
                return JsonResponse(
                    {"status": "error", "message": "entity_pid is not exist"}
                )

            if len(acc.pids) == 0:

                # 系统内没有计算的证据值
                for entity_pid in json_data:
                    # 先加入到pids中，再分别计算witness，避免witness重复更新
                    acc.add_member(entity_pid)
                print(acc.pids)

                # acc.add_member(entity_pid)
                not_send_list = []
                for entity_pid in json_data:
                    temp_parcialkey: str = acc.witness_generate_by_pid(entity_pid)
                    # 写入数据库保存
                    entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
                    entity_instance.entity_parcialkey = temp_parcialkey
                    # 将部分私钥发送给要存储的ap
                    payload = {
                        "patcialkey_data": {
                            "entity_pid": entity_pid,
                            "entity_parcialkey": temp_parcialkey,
                            "acc_cur": utils.int2hex(acc.acc_cur),
                        }
                    }
                    node_ip = entity_instance.node_id.node_ip
                    node_port = entity_instance.node_id.node_port
                    if not entity_instance.node_id.node_is_alive:
                        not_send_list.append(entity_pid)
                        continue

                    response = post_to_ap(
                        node_ip,
                        node_port,
                        "/entitymanage/getparcialkey/",
                        payload=payload,
                    )

                    # ap掉线情况,继续发送后面的数据，掉线信息记录
                    if response == None:
                        not_send_list.append(entity_pid)
                        continue

                    if response.json()["status"] != "success":
                        acc.pids = []
                        return JsonResponse(
                            {"status": "error", "message": response.json()["message"]}
                        )

                    # 将信息保存到as本地数据库
                    entity_instance.save()
                # 将kgc的信息保存
                kgc_paramter_save()
                print("test")
                if len(not_send_list) != 0:
                    return JsonResponse(
                        {"status": "sucess", "message": "{}".format(not_send_list)}
                    )
                return JsonResponse({"status": "success"})

            else:
                for entity_pid in json_data:
                    # 先加入到pids中，再分别计算witness，避免witness重复更新
                    if entity_pid in acc.pids:
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "entity_pid is already exist",
                            }
                        )

                    acc.add_member(entity_pid)

                # acc.add_member(entity_pid)
                print(acc.pids)
                print(json_data)
                # 计算聚合后的aux
                aux = acc.get_new_aux(json_data)
                print(aux)
                # 向存活的ap发送aux
                node_instance_all = NodeTable.objects.filter(node_is_alive=True)
                for tmp_node in node_instance_all:
                    node_ip = tmp_node.node_ip
                    node_port = tmp_node.node_port
                    payload = {
                        "aux_data": {
                            "aux": aux,
                            "acc_cur": utils.int2hex(acc.acc_cur),
                        }
                    }
                    response = post_to_ap(
                        node_ip,
                        node_port,
                        "/entitymanage/getauxdata/",
                        payload=payload,
                    )
                    if response.json()["status"] != "success":
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": response.json()["message"],
                            }
                        )
                # 更新本地现存的部分私钥
                entity_parcialkey_instance = EnityTable.objects.filter(
                    entity_parcialkey__isnull=False
                )
                for tmp_instance in entity_parcialkey_instance:
                    tmp_instance.entity_parcialkey = acc.update_witness(
                        aux, tmp_instance.entity_parcialkey
                    )
                    tmp_instance.save()

                # 计算新增的部分私钥
                not_send_list = []
                for entity_pid in json_data:
                    temp_parcialkey: str = acc.witness_generate_by_pid(entity_pid)
                    # 写入数据库保存
                    entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
                    entity_instance.entity_parcialkey = temp_parcialkey
                    # 将部分私钥发送给要存储的ap
                    payload_parcialkey = {
                        "patcialkey_data": {
                            "entity_pid": entity_pid,
                            "entity_parcialkey": temp_parcialkey,
                            "acc_cur": utils.int2hex(acc.acc_cur),
                        }
                    }
                    node_ip = entity_instance.node_id.node_ip
                    node_port = entity_instance.node_id.node_port
                    if not entity_instance.node_id.node_is_alive:
                        not_send_list.append(entity_pid)
                        continue

                    response = post_to_ap(
                        node_ip,
                        node_port,
                        "/entitymanage/getparcialkey/",
                        payload=payload_parcialkey,
                    )

                    # ap掉线情况,继续发送后面的数据，掉线信息记录
                    if response == None:
                        not_send_list.append(entity_pid)
                        continue

                    if response.json()["status"] != "success":
                        acc.pids = []
                        return JsonResponse(
                            {"status": "error", "message": response.json()["message"]}
                        )
                    entity_instance.save()

                kgc_paramter_save()
                if len(not_send_list) != 0:
                    return JsonResponse(
                        {"status": "sucess", "message": "{}".format(not_send_list)}
                    )
                return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 撤销实体
@csrf_exempt
def entity_withdraw(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("withdraw_pid")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            entity_pid = json_data.get("entity_pid")
            entity_instace = EnityTable.objects.get(entity_pid=entity_pid)
            if entity_instace != None:
                # 向对应的ap发送删除请求
                # 判断ap是否alive
                if not entity_instace.node_id.node_is_alive:
                    return JsonResponse({"status": "error", "message": "ap not alive"})
                node_ip = entity_instace.node_id.node_ip
                node_port = entity_instace.node_id.node_port
                payload = {"withdraw_data": {"entity_pid": entity_pid}}
                response = post_to_ap(
                    node_ip,
                    node_port,
                    "/entitymanage/getwithdrawdata/",
                    payload=payload,
                )
                # ap可能掉线，掉线返回错误，不保存数据
                if response == None:
                    return JsonResponse({"status": "error", "message": "ap not alive"})

                if response.json()["status"] != "success":
                    return JsonResponse(
                        {"status": "error", "message": response.json()["message"]}
                    )

                if entity_instace.entity_parcialkey != None:
                    # 如果entity计算过部分私钥，更新accumulator，并且计算aux，并发送给全体节点
                    aux = acc.remove_member(entity_pid)
                    # 将aux发送给全部AP nodes
                    node_instance_all = NodeTable.objects.filter(node_is_alive=True)
                    for tmp_node in node_instance_all:
                        node_ip = tmp_node.node_ip
                        node_port = tmp_node.node_port
                        payload = {
                            "aux_data": {
                                "aux": aux,
                                "acc_cur": utils.int2hex(acc.acc_cur),
                            }
                        }
                        response = post_to_ap(
                            node_ip,
                            node_port,
                            "/entitymanage/getauxdata/",
                            payload=payload,
                        )
                        if response.json()["status"] != "success":
                            return JsonResponse(
                                {
                                    "status": "error",
                                    "message": response.json()["message"],
                                }
                            )

                    # 更新AS上的部分私钥记录
                    temp_pids = EnityTable.objects.filter(
                        entity_parcialkey__isnull=False
                    )
                    for tmp in temp_pids:
                        tmp.entity_parcialkey = acc.update_witness(
                            aux, tmp.entity_parcialkey
                        )
                        tmp.save()
                # 撤销删除操作完成
                entity_instace.delete()
                kgc_paramter_save()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "pid not exists"})

        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


# 发送公共参数
def send_public_parameter(request):
    if request.method == "POST":
        node_entity = NodeTable.objects.get(node_ip=request.META.get("REMOTE_ADDR"))
        if node_entity == None:
            return JsonResponse({"status": "error", "message": "node not exists"})
        data = {
            "kgc_id": "kgc_id",
            "acc_publickey": acc.get_publickey(),
            "acc_cur": acc.get_acc_cur(),
            "kgc_q": kgc.get_q(),
            "kgc_Ppub": kgc.get_Ppub(),
        }
        node_entity.node_is_alive = True
        node_entity.save()
        return JsonResponse({"status": "success", "message": data})


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


def post_to_ap(node_ip: str, node_port: int, path: str, payload: dict):
    header = {"content-type": "application/json", "Connection": "close"}
    url = "http://" + node_ip + ":" + str(node_port) + path
    data = json.dumps(payload)
    try:
        res = requests.post(url, data=data, headers=header)
        print(res.status_code)
        return res
    except Exception as e:
        node_instance = NodeTable.objects.get(node_ip=node_ip)
        node_instance.node_is_alive = False
        node_instance.save()
        print(e)
        return None
