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
from fastecdsa import curve, keys
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
acc.cur = utils.hex2int(temp_params.kgc_acc_cur)
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
            kgc_instance.kgc_acc_serectkey0 = acc.get_serect_key()
            kgc_instance.kgc_acc_serectkey1 = acc.get_serect_key()
            kgc_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def kgc_paramter_save():
    kgc_instance = KGCParamterTable.objects.filter(kgc_id="kgc_id")
    kgc_instance.kgc_s = kgc.get_s()
    kgc_instance.kgc_Ppub = kgc.get_Ppub()
    kgc_instance.kgc_q = kgc.get_q()
    kgc_instance.kgc_acc_G = acc.get_G()
    kgc_instance.kgc_acc_publickey = acc.get_publickey()
    kgc_instance.kgc_acc_cur = acc.get_acc_cur()
    kgc_instance.kgc_acc_serectkey0 = acc.get_serect_key()
    kgc_instance.kgc_acc_serectkey1 = acc.get_serect_key()
    kgc_instance.save()


def getToken(request):
    token = get_token(request)
    return HttpResponse(
        json.dumps({"token": token}), content_type="application/json,charset=utf-8"
    )


def entity_query_alive(request):
    """
    return alive nodes
    """
    if request.method == "POST":
        try:
            query_instance = EnityTable.objects.filter(is_alive=True)

            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
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
            json_data = request.POST.get("add_data")
            json_data = json.loads(json_data)
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
            json_data = request.POST.get("query_data")
            json_data = json.loads(json_data)
            entity_pid = json_data["entity_pid"]
            query_instance = EnityTable.objects.get(entity_pid=entity_pid)
            data = query_instance.get_data()
            return JsonResponse({"status": "success", "message": data})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def entity_query_all(request):
    if request.method == "POST":
        try:
            query_instance = EnityTable.objects.all()
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 计算实体的部分私钥
def entity_calculate_parcialkey(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("calculate_data")
            json_data = json.loads(json_data)
            if len(acc.pids) == 0:
                # 系统内没有计算的证据值
                for temp in json_data:
                    # 先加入到pids中，再分别计算witness，避免witness重复更新
                    entity_pid = temp["entity_pid"]
                    acc.add_member(entity_pid)
                print(acc.pids)

                for temp in json_data:
                    entity_pid = temp["entity_pid"]
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
                    response = post_to_ap(
                        node_ip,
                        node_port,
                        "/entitymanage/getparcialkey/",
                        payload=payload,
                    )

                    # ap掉线情况未考虑，后面改
                    if response.json()["status"] != "success":
                        acc.pids = []
                        return JsonResponse(
                            {"status": "error", "message": response.json()["message"]}
                        )
                    # 将信息保存到as本地数据库
                    entity_instance.save()
                # 将kgc的信息保存
                # acc.save_accumlator_parameters("accumulator.json")
                kgc_paramter_save()
                return JsonResponse({"status": "success"})

            else:
                print("待完善")
                return JsonResponse({"status": "success", "message": "wait add"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 撤销实体
@csrf_exempt
def entity_withdraw(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("withdraw_pid")
            json_data = json.loads(json_data)
            entity_pid = json_data.get("entity_pid")
            entity_instace = EnityTable.objects.get(entity_pid=entity_pid)

            if entity_instace != None:
                # 向对应的ap发送删除请求
                node_ip = entity_instace.node_id.node_ip
                node_port = entity_instace.node_id.node_port
                payload = {"withdraw_data": {"entity_pid": entity_pid}}
                response = post_to_ap(
                    node_ip,
                    node_port,
                    "/entitymanage/getwithdrawdata/",
                    payload=payload,
                )
                # ap可能掉线，后面改
                if response.json()["status"] != "success":
                    return JsonResponse(
                        {"status": "error", "message": response.json()["message"]}
                    )

                if entity_instace.entity_parcialkey != None:
                    # 如果entity计算过部分私钥，更新accumulator，并且计算aux，并发送给全体节点
                    aux = acc.remove_member(entity_pid)

                    # 将aux发送给全部AP nodes
                    node_instance_all = NodeTable.objects.all()
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
                # acc.save_accumlator_parameters("accumulator.json")
                kgc_paramter_save()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "pid not exists"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 发送公共参数
def send_public_parameter(request):
    if (
        NodeTable.objects.get(node_ip=request.META.get("REMOTE_ADDR")) != None
        and request.method == "POST"
    ):
        data = {
            "kgc_id": "kgc_id",
            "acc_publickey": acc.get_publickey,
            "acc_cur": acc.get_acc_cur,
            "kgc_q": kgc.get_q,
            "kgc_Ppub": kgc.get_Ppub,
        }
        return JsonResponse({"status": "success", "message": data})


# 从ap获取存活实体的pid
@csrf_exempt
def get_alive_entity_pid(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("entity_data")
            entity_pid = json_data["entity_pid"]
            entity_instance = EnityTable.objects.get(entity_pid=entity_pid)
            entity_instance.is_alive = True
            entity_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": "error"})


def post_to_ap(node_ip: str, node_port: int, path: str, payload: dict):
    header = {"content-type": "application/json"}
    url = "http://" + node_ip + ":" + str(node_port) + path
    data = json.dumps(payload)
    res = requests.post(url, data=data, headers=header)
    print(res.status_code)
    return res
