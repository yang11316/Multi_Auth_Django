from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
import json
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt
import time

from commonutils import KGC
from commonutils import utils


# Create your views here.


kgc = KGC.KGC()
paramters_instance = PublicParamtersTable.objects.get(kgc_id="kgc_id")
kgc.acc_cur = utils.hex2int(paramters_instance.acc_cur)
kgc.acc_publickey = utils.hex2int(paramters_instance.acc_publickey)
kgc.kgc_q = utils.hex2int(paramters_instance.kgc_q)
kgc.kgc_Ppub = utils.hex2int(paramters_instance.kgc_Ppub)


AS_ip = "192.168.3.17"
AS_port = 8000

"""与AS交互"""
# 获取传来的公共参数
def get_public_paramters(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("data")
            pubparamter_instance = PublicParamtersTable.objects.get(
                kgc_id=json_data.get("kgc_id")
            )
            pubparamter_instance.acc_cur = json_data.get("acc_cur")
            pubparamter_instance.acc_publickey = json_data.get("acc_publickey")
            pubparamter_instance.kgc_q = json_data.get("kgc_q")
            pubparamter_instance.kgc_Ppub = json_data.get("kgc_Ppub")
            pubparamter_instance.save()
        except Exception as e:
            print(e)

def save_kgc_paramters():
    paramters_instance = PublicParamtersTable.objects.get(kgc_id="kgc_id")
    paramters_instance.acc_cur = kgc.acc_cur
    paramters_instance.acc_publickey = kgc.acc_publickey
    paramters_instance.kgc_q = kgc.q
    paramters_instance.kgc_Ppub = kgc.Ppub
    paramters_instance.save()

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
                software_hash=json_data["software_hash"],
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
            kgc.acc_cur = utils.hex2int(acc_cur)
            entity_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
# 接收as发来的撤销信息 {"withdrew_data":{"entity_pid":""}}
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
            kgc.acc_cur=utils.hex2int(kgc.update_witness(aux_data,utils.int2hex(kgc.acc_cur)))
            save_kgc_paramters()
            # 将aux分别发送给alive进程,待完成
            print(utils.int2hex(kgc.acc_cur))
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
        

        
"""发送给process"""
# 收到进程请求部分密钥或者pi请求，查看是否存在pid，发送部分密钥和公平参数，修改entity的alive状态，并上报as
@csrf_exempt
def send_particalkey_and_pid(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("entity_pid")
            entity_port = request.POST.get("port")
            # json_data = json.loads(json_data)
            process_ip:str = request.META.get("REMOTE_ADDR")
            # process_port:int = 9999
            print(json_data)
            print(process_ip,entity_port)
            entity_instance = EntityInfo.objects.get(entity_pid = json_data)
            entity_pid = json_data
            
            # 不存在注册的进程就返回空的http请求
            if entity_instance == None:                
                return HttpResponse()
            # 发送pid和公共参数
            if entity_instance.entity_parcialkey == None:
                data = {
                    "acc_publickey":utils.int2hex(kgc.acc_publickey),
                    "pid":entity_instance.entity_pid,
                    "acc_cur":utils.int2hex(kgc.acc_cur),
                    "kgc_Ppub":utils.int2hex(kgc.kgc_Ppub),
                    }
                print("send without parcialkey")
                time.sleep(1)
                post_data_to_process(process_ip,entity_port,"",data)
                
            # 进程索要部分私钥的时候认为进程为alive
            else:
                entity_instance.is_alive = True
                data = {
                    "acc_publickey":utils.int2hex(kgc.acc_publickey),
                    "pid":entity_instance.entity_pid,
                    "acc_cur":utils.int2hex(kgc.acc_cur),
                    "kgc_Ppub":utils.int2hex(kgc.kgc_Ppub),
                    "entity_parcialkey": entity_instance.entity_parcialkey
                }
                
                # 存活实体上报给as
                post_as_data = {"entity_data":{
                    "entity_pid": entity_pid
                    }
                }
                post_data(AS_ip,AS_port,"/entitymanage/getaliveentity/",post_as_data)
                entity_instance.save()
                time.sleep(1)
                print("send parcialkey")
                post_data_to_process(process_ip,entity_port,"",data)
            time.sleep(1)
            return HttpResponse("ok")
        except Exception as e:
            print("error")
            return HttpResponse("error")
        
        
def post_data(ip: str,port:int, path: str,payload: dict):
    try:
        header = {"content-type": "application/json"}
        data = json.dumps(payload)
        url = "http://"+ip+":"+str(port)+path
        res = requests.post(url, data=data, headers=header)
        print(res.text)
    except Exception as e:
        print(e)

def post_data_to_process(ip: str,port:str, path: str,payload: dict):
    
    try:
        url = "http://"+ip+":"+port+path
        print(url)
        res=requests.post(url, data=payload)
        print(res.text)
    except Exception as e:
        print(e)