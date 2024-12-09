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
from commonutils import switch_interface
import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job

# Create your views here.

AS_ip = settings.AS_IP
AS_port = settings.AS_PORT

# 与as同步最新数据
try:
    header = {"content-type": "application/json","Connection":"close"}
    url = "http://"+AS_ip+":"+str(AS_port)+"/entitymanage/get-public-parameter/"
    res = requests.post(url, headers=header)
    json_data = res.json()
    
    pubparamter_instance = PublicParamtersTable.objects.get(
        kgc_id="kgc_id"
    )
    pubparamter_instance.acc_cur = json_data["message"]["acc_cur"]
    pubparamter_instance.acc_publickey = json_data["message"]["acc_publickey"]
    pubparamter_instance.kgc_q = json_data["message"]["kgc_q"]
    pubparamter_instance.kgc_Ppub = json_data["message"]["kgc_Ppub"]
    pubparamter_instance.domain_id = json_data["message"]["domain_id"]
    pubparamter_instance.save()
    print("get public parameters success")

except Exception as e:
    print("get public parameters failed")
    print(e)


kgc = KGC.KGC()
paramters_instance = PublicParamtersTable.objects.get(kgc_id="kgc_id")
kgc.acc_cur = utils.hex2int(paramters_instance.acc_cur)
kgc.acc_publickey = utils.hex2int(paramters_instance.acc_publickey)
kgc.kgc_q = utils.hex2int(paramters_instance.kgc_q)
kgc.kgc_Ppub = utils.hex2int(paramters_instance.kgc_Ppub)
kgc.domain_id = paramters_instance.domain_id




scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(),"default")

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
        res = requests.post(url, data=data, headers=header)
        return res
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
            pubparamter_instance.domain_id = json_data.get("domain_id")
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


@csrf_exempt
def get_entity(request):
    if request.method=="POST":
        try:
            json_data = request.body.decode("utf-8")
            # print(json_data)
            json_data = json.loads(json_data)
            software_id = json_data["software_id"]
            software_hash = json_data["software_hash"]
            user_id = json_data["user_id"]
            entity_ipaddr = json_data["entity_ip"]
            acc_cur = json_data["acc_cur"]
            aux_data = json_data["aux"]
            entity_pair=json_data["entity_pair"]
            kgc.acc_cur = utils.hex2int(acc_cur)
            save_kgc_paramters()
            print("update now")
            print(aux_data)
            # 更新现有的进程的部分私钥
            for entity_instance in EntityInfo.objects.filter(entity_parcialkey__isnull=False):
                entity_instance.entity_parcialkey = kgc.update_witness(aux_data,entity_instance.entity_parcialkey)
                entity_instance.save()
            # 将aux分别发送给alive进程    
            sended_list=[]
            for entity in EntityInfo.objects.filter(is_alive=True): 
                entity_ip = entity.entity_ip
                entity_listening_port = str(entity.entity_listening_port)
                if entity_listening_port in sended_list:
                    continue
                sended_list.append(entity_listening_port)
                data={"aux":aux_data}
                post_data_to_process(entity_ip,entity_listening_port,"",data)
            # 创建新的entity
            # print(entity_pair)
            for tmp_pair in entity_pair:
                if(EntityInfo.objects.filter(entity_pid=tmp_pair["entity_pid"]).exists()):
                    entity_instance = EntityInfo.objects.get(entity_pid=tmp_pair["entity_pid"])
                    entity_instance.entity_parcialkey = tmp_pair["entity_parcialkey"]
                    entity_instance.software_hash = software_hash
                    entity_instance.software_id = software_id
                    entity_instance.user_id = user_id
                    entity_instance.entity_ip = entity_ipaddr
                    entity_instance.save()
                    continue
                entity_instance = EntityInfo()
                entity_instance.entity_pid = tmp_pair["entity_pid"]
                entity_instance.software_hash = software_hash
                entity_instance.software_id = software_id
                entity_instance.user_id = user_id
                entity_instance.entity_ip = entity_ipaddr
                entity_instance.entity_parcialkey = tmp_pair["entity_parcialkey"]
                entity_instance.save()
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


# 接收as发来的更新凭证 {"aux_data":{"aux":""}}
@csrf_exempt
def get_aux_data(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data).get("aux_data")
            aux_data = json_data["aux"]
            withdraw_pid = json_data["withdraw_pid"]
            # 首先查看本地是否存在要删除的pid
            entity_instance = EntityInfo.objects.filter(entity_pid=withdraw_pid).exists()
            if(entity_instance):
                entity_instance = EntityInfo.objects.get(entity_pid=withdraw_pid)
                entity_instance.delete()
                print("delete entity:"+withdraw_pid)
            print("get aux data:"+aux_data)
            # 更新本地acc_cur
            kgc.acc_cur=utils.hex2int(kgc.update_witness(aux_data,utils.int2hex(kgc.acc_cur)))
            save_kgc_paramters()
            # 更新进程的部分私钥
            for entity_instance in EntityInfo.objects.filter(entity_parcialkey__isnull=False):
                entity_instance.entity_parcialkey = kgc.update_witness(aux_data,entity_instance.entity_parcialkey)
                entity_instance.save()
            # 将aux分别发送给alive进程
            sended_port=[]
            for entity in EntityInfo.objects.filter(is_alive=True): 
                entity_ip = entity.entity_ip
                entity_listening_port = str(entity.entity_listening_port)
                if entity_listening_port in sended_port:
                    continue
                sended_port.append(entity_listening_port)
                data={"aux":aux_data,"pid":withdraw_pid}
                post_data_to_process(entity_ip,entity_listening_port,"",data)
            sended_port.clear()
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
                        "entity_parcialkey": entity.entity_parcialkey,

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
                    
            response_data = {"entity_data":ret_data,"domain_id":kgc.domain_id}
            # print(response_data)
            return JsonResponse(response_data)
        except Exception as e:
            print(e)
            return HttpResponse("error")
        

# 接收进程发来的domian_id，并向as发送询问
@csrf_exempt
def get_domain_parameters(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            domain_id = json_data["domain_id"]
            payload = {"domain_id":domain_id}
            ret = post_data(AS_ip,AS_port,"/domainmanage/get-domain-key/",payload)
            return JsonResponse(ret.json())
        except Exception as e:
            print(e)
            return HttpResponse("error")
        
# 接收进程发来的dds请求，首先将请求发送AS验证，随后发送RFAC报文
@csrf_exempt        
def get_dds_info(request):
    if request.method == "POST":
        try:
            json_data =  request.body.decode("utf-8")
            # print(json_data)
            json_data = json.loads(json_data)
            entity_pid = json_data["entity_pid"]
            if not EntityInfo.objects.filter(entity_pid=entity_pid).exists():
                return JsonResponse({"status":"error","message":"no such entity"})
            print(json_data)
            validator = switch_interface.RequestDataValidator(json_data)
            validation_errors = validator.validate()
            if validation_errors:
                return JsonResponse(
                    {"status": "error", "message": ", ".join(validation_errors)}
                )
            ret = post_data(AS_ip,AS_port,"/ddsmanage/get-dds-info/",json_data)
            ret_data = ret.json()
            # AS返回error，则返回错误信息到进程
            print(ret_data)
            if ret_data["status"]!="success":
                return HttpResponse("error")
            
            PacketID = ret_data["message"]
            # 发送rfac报文
            dds_type = json_data.get("dds_type")
            protocol_type = json_data.get("protocol_type")
            source_ip = json_data.get("source_ip")
            source_port = json_data.get("source_port")
            source_mask = json_data.get("source_mask")
            source_mac = json_data.get("source_mac")
            destination_ip = json_data.get("destination_ip")
            destination_port = json_data.get("destination_port")
            destination_mask = json_data.get("destination_mask")
            destination_mac = json_data.get("destination_mac")
            # code : 1 permit  packet_id : 递增 sid : 1
            rfac_packet = switch_interface.RFACPacket(
                code=1,
                packet_id=PacketID,
                sid=1,
            )
            # 构造RFAC报文
            # 设置protocol值  dds_type: 1 publisher 2 subscriber   protocol_type: 1tcp  2udp
            if dds_type == 1:
                if protocol_type == 1:
                    rfac_packet.set_protocol(6)
                elif protocol_type == 2:
                    rfac_packet.set_protocol(17)
            else:
                rfac_packet.set_protocol(2)

            rfac_packet.set_ip(1, source_ip)
            rfac_packet.set_port(2, source_port)
            rfac_packet.set_mask(3, source_mask)
            rfac_packet.set_ip(4, destination_ip)
            rfac_packet.set_port(5, destination_port)
            rfac_packet.set_mask(6, destination_mask)
            rfac_packet.set_mac(8, source_mac)
            rfac_packet.set_mac(9, destination_mac)
            pack_data = rfac_packet.build()
            switch_interface.send_raw_packet(pack_data, settings.SWITHCH_MAC)
            return HttpResponse("success")
        except Exception as e:
            print(e)
            return HttpResponse("error")


