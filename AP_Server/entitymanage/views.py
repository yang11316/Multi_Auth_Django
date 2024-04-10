from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt

from commonutils import accumulator
from commonutils import utils

# Create your views here.


acc = accumulator.Accumulator()
# 注册实体时接收as发来信息，未授予部分密钥
@csrf_exempt
def get_entity_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("add_data")
            print(json_data)
            EntityInfo.objects.create(
                entity_pid=json_data["entity_pid"],
                software_id=json_data["software_id"],
                user_id=json_data["user_id"],
                entity_ip=json_data["entity_ip"],
            )
            
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

# 接收as发来的部分私钥{"patcialkey_data":{"entity_pid":"","entity_porecessid":""}}
@csrf_exempt
def get_parcial_key(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("patcialkey_data")
            # print(json_data)
            entity_instance = EntityInfo.objects.get(entity_pid = json_data["entity_pid"])
            entity_instance.entity_parcialkey = json_data["entity_parcialkey"]
            acc_cur = json_data["acc_cur"]
            acc.acc_cur = utils.hex2int(acc_cur)
            entity_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})



@csrf_exempt# 接收as发来的撤销信息 {"withdrew_data":{"entity_pid":""}}
def get_withdraw_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("withdraw_data")
            print(json_data["entity_pid"])
            entity_instance = EntityInfo.objects.get(entity_pid = json_data["entity_pid"])
            entity_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
# 接收as发来的更新凭证 {"aux_data":{"aux_data":""}}
@csrf_exempt
def get_aux_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("aux_data")
            aux_data = json_data["aux"]
            # 更新本地acc_cur
            acc.acc_cur=utils.hex2int(acc.update_witness(aux_data,utils.int2hex(acc.acc_cur)))

            # 将aux分别发送给alive进程
            print(utils.int2hex(acc.acc_cur))
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
        
# 收到进程请求部分密钥请求，发送部分密钥，修改entity的alive状态，并上报as

def send_partical_key(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("entity_pid")
            print(json_data)
            entity_instance = EntityInfo.objects.get(entity_pid = json_data["entity_pid"])
            if entity_instance.entity_parcialkey == None:
                return JsonResponse({"status": "error", "message": "no parcialkey"})
            entity_instance.is_alive = True

            return JsonResponse({"status": "success", "entity_parcialkey": entity_instance.entity_parcialkey})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
        

def post_data(ip: str,port:str, payload: dict):
    header = {"content-type": "application/json"}
    data = json.dumps(payload)
    url = f"http://{ip}:{port}"
    res = requests.post(url, data=data, headers=header)
    print(res.text)