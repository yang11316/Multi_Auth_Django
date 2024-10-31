from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.conf import settings
import json
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt
import time
from commonutils import KGC
from commonutils import utils
import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job

# Create your views here.


kgc = KGC.KGC()
paramters_instance = PublicParamtersTable.objects.get(kgc_id="kgc_id")
kgc.acc_cur = utils.hex2int(paramters_instance.acc_cur)
kgc.acc_publickey = utils.hex2int(paramters_instance.acc_publickey)
kgc.kgc_q = utils.hex2int(paramters_instance.kgc_q)
kgc.kgc_Ppub = utils.hex2int(paramters_instance.kgc_Ppub)


AS_ip = settings.AS_IP
AS_port = settings.AS_PORT

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(),"default")

# def check_process_alive(processid:int):
#     try:
#         return psutil.pid_exists(processid)

#     except Exception as e:
#         return False

# bug fix: 修复活跃实体同步不到的问题，在调用时强转
def check_process_alive(processid):
    try:
        return psutil.pid_exists(processid)

    except Exception as e:
        print(e)
        return False
def post_data(ip: str,port:int, path: str,payload: dict):
    try:
        header = {"content-type": "application/json","Connection":"close"}
        data = json.dumps(payload)
        url = "http://"+ip+":"+str(port)+path
        print(url)
        res = requests.post(url, data=data, headers=header)
        print(res.text)
    except Exception as e:
        print(e)

def post_data_to_process(ip: str,port:str, path: str,payload: dict):
    try:
        header = {"Connection":"close"}
        url = "http://"+ip+":"+port+path
        print(url)
        res=requests.post(url, data=payload,headers=header)
        print(res.text)

    except Exception as e:
        print(e)   

@register_job(scheduler,'interval',seconds=60,id='check_entity_alive',replace_existing=True)
def schedluer_job():
    entity_instance = EntityInfo.objects.filter(is_alive=True)
    entity_pid_list=[]
    for entity in entity_instance:
        if not check_process_alive(int(entity.entity_porecessid)):
            entity.is_alive = False
            entity.entity_porecessid = ""
            entity.entity_listening_port = 0
            entity.entity_sending_port = 0
            entity_pid_list.append(entity.entity_pid)
            entity.save()
    print(entity_pid_list)
    if(len(entity_pid_list)!=0):
        data={
            "entity_data":{
                "entity_pid":entity_pid_list
            }  
        }
        post_data(AS_ip,AS_port,"/entitymanage/get-down-entity/",data)
scheduler.start()



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
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})

def save_kgc_paramters():
    paramters_instance = PublicParamtersTable.objects.get(kgc_id="kgc_id")
    paramters_instance.acc_cur = utils.int2hex(kgc.acc_cur)
    paramters_instance.acc_publickey = utils.int2hex(kgc.acc_publickey)
    paramters_instance.kgc_q = utils.int2hex(kgc.kgc_q)
    paramters_instance.kgc_Ppub = utils.int2hex(kgc.kgc_Ppub)
    paramters_instance.save()

# 注册实体时接收as发来信息，未授予部分密钥
@csrf_exempt
def get_entity_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("add_data")
            print("get entity data:"+json_data["entity_pid"])
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
            save_kgc_paramters()
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
            print("withdrew entity pid:"+json_data["entity_pid"])
            entity_instance = EntityInfo.objects.get(entity_pid = json_data["entity_pid"])
            entity_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
# 接收as发来的更新凭证 {"aux_data":{"aux":""}}
@csrf_exempt
def get_aux_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("aux_data")
            aux_data = json_data["aux"]
            print("get aux data:"+aux_data)
            # 更新本地acc_cur
            kgc.acc_cur=utils.hex2int(kgc.update_witness(aux_data,utils.int2hex(kgc.acc_cur)))
            save_kgc_paramters()

            # 更新进程的部分私钥
            for entity_instance in EntityInfo.objects.filter(entity_parcialkey__isnull=False):
                entity_instance.entity_parcialkey = kgc.update_witness(aux_data,entity_instance.entity_parcialkey)
                entity_instance.save()
            # 将aux分别发送给alive进程
            for entity in EntityInfo.objects.filter(is_alive=True):
                
                entity_ip = entity.entity_ip
                entity_listening_port = str(entity.entity_listening_port)
                data={"aux":aux_data}
                post_data_to_process(entity_ip,entity_listening_port,"",data)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
        

        
"""发送给process"""
# 收到进程请求部分密钥或者pid请求，查看是否存在pid，发送部分密钥和公平参数，修改entity的alive状态，并上报as
@csrf_exempt
def send_particalkey_and_pid(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)        
            entity_processid = json_data["process_id"]
            entity_listening_port = json_data["listening_port"]
            entity_sending_port=json_data["sending_port"]
            # json_data = json.loads(json_data)
            process_ip:str = request.META.get("REMOTE_ADDR")
            
            entity_path = utils.get_process_path(int(entity_processid))
            entity_hash = utils.calculate_file_hash(entity_path)
            print(process_ip,entity_listening_port,entity_sending_port,entity_processid,entity_path,entity_hash)
            in_entityinfo = EntityInfo.objects.filter(software_hash=entity_hash).exists()

            # 不存在注册的进程就返回空的http请求
            if not in_entityinfo :    
                print("not entity")            
                return HttpResponse("error")
            # 发送pid和公共参数

            ret_data=[]
            entity_instance = EntityInfo.objects.filter(software_hash=entity_hash)
            for entity in entity_instance:
                if entity.entity_parcialkey != None:
                    ret_data.append({
                        "acc_publickey":utils.int2hex(kgc.acc_publickey),
                        "pid":entity.entity_pid,
                        "acc_cur":utils.int2hex(kgc.acc_cur),
                        "kgc_Ppub":utils.int2hex(kgc.kgc_Ppub),
                        "entity_parcialkey": entity.entity_parcialkey
                    })   
                    entity.is_alive = True
                    entity.entity_porecessid = entity_processid
                    entity.entity_listening_port = entity_listening_port
                    entity.entity_sending_port = entity_sending_port
                    entity.save() 
                    # 存活实体上报给as
                    post_as_data = {"entity_data":{
                        "entity_pid": entity.entity_pid,
                        "entity_sending_port":entity_sending_port,
                        "entity_listening_port":entity_listening_port,
                        "entity_processid":entity.entity_porecessid
                        }
                    }
                    post_data(AS_ip,AS_port,"/entitymanage/get-alive-entity/",post_as_data)
                    
            # print("send parcialkey")
            # post_data_to_process(process_ip,entity_listening_port,"",data)
            response_data = {"entity_data":ret_data}
            return JsonResponse(response_data)
        except Exception as e:
            print(e)
            return HttpResponse("error")
        
@csrf_exempt
def get_open_port(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            print(json_data)
            open_port = json_data["open_port"]
            process_id = json_data["process_id"]
            
            # 判断数据库中是否存在这个进程
            entity_path = utils.get_process_path(int(process_id))
            print(entity_path)
            entity_hash = utils.calculate_file_hash(entity_path)
            print(entity_hash)
            entity_instance = EntityInfo.objects.filter(software_hash=entity_hash).exists()
            # 不存在注册的进程就返回空的http请求
            if not entity_instance :    
                print("not such entity")            
                return HttpResponse("error")
            # 进行打开端口的操作
            print(open_port)
            return HttpResponse("success")
        except Exception as e:
            print(e)
            return HttpResponse("error")
