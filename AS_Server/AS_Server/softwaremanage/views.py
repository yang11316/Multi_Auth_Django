from django.http import JsonResponse
from django.shortcuts import render
from commonutils.utils import *
from usermanage.models import *
from .models import *
from commonutils import utils
from entitymanage.models import EnityTable
from nodemanage.models import NodeTable
from django.utils import timezone
import requests
import json


# Create your views here.


def registsoftware_add(request):
    if request.method == "POST":
        """
        add_data:{
            "rsoftware_name":"",
            "rsoftware_path":"",
            "rsoftware_version":"",
            "rsoftware_desc":"",
            "user_id":"",
            "location_data":[
                {
                    "node_ip":"",
                    "entity_ip":""
                }
            ]
        }
        
        """
        try:
            # json_data = request.POST.get("add_data")
            json_data = json.loads(request.body.decode("utf-8"))
            # 获取数据
            rsoftware_instace = RegisterSoftwareTable()
            rsoftware_instace.rsoftware_id = calculate_str_hash(
                json_data["rsoftware_name"] + json_data["rsoftware_version"]
            )
            rsoftware_instace.rsoftware_name = json_data["rsoftware_name"]
            rsoftware_instace.rsoftware_path = (
                "/home/default/file_upload/" + json_data["rsoftware_name"]
            )
            rsoftware_instace.rsoftware_version = json_data["rsoftware_version"]
            rsoftware_instace.rsoftware_desc = json_data["rsoftware_desc"]
            user_id = json_data["user_id"]
            user_instance = UserTable.objects.get(user_id=user_id)
            if(user_instance == None):
                return JsonResponse({"status": "add error failed", "message": "user not exist"})
            rsoftware_instace.user_id = user_instance
            rsoftware_instace.create_time = timezone.now()
            rsoftware_instace.save()

            # 保存注册的location信息
            location_data = json_data["location_data"]
            for tmp in location_data:
                if(RegisterSoftwareLocationTable.objects.filter(entity_ip = tmp["entity_ip"],rsoftware_id = rsoftware_instace.rsoftware_id).exists()):
                    continue
                rsoftwarelocation_instace = RegisterSoftwareLocationTable()
                rsoftwarelocation_instace.rsoftware_id = rsoftware_instace
                # rsoftwarelocation_instace.node_ip = tmp["node_ip"]
                rsoftwarelocation_instace.node_ip = tmp["entity_ip"]
                rsoftwarelocation_instace.entity_ip = tmp["entity_ip"]
                rsoftwarelocation_instace.create_time = timezone.now()
                rsoftwarelocation_instace.save()
            return JsonResponse({"status": "success"})

        except Exception as e:
            print(e)
            return JsonResponse({"status": "add error failed", "message": str(e)})

def registsoftware_query_all(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = RegisterSoftwareTable.objects.all()
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

def registsoftware_query_by_id(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("query_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            rsoftware_id = json_data["rsoftware_id"]
            query_instance = RegisterSoftwareTable.objects.filter(
                rsoftware_id=rsoftware_id
            )
            if query_instance.count() == 0:
                return JsonResponse({"status": "error", "message": "not exist"})
            data = query_instance.get_data()
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def registsoftwarelocation_query_by_id(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("query_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            rsoftware_id=json_data["rsoftware_id"]
            query_instance = RegisterSoftwareLocationTable.objects.filter(rsoftware_id=rsoftware_id)
            if query_instance.count() == 0:
                return JsonResponse({"status": "error", "message": "rsoftware_id not exist"})
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance]
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def registsoftwarelocation_query_all(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = RegisterSoftwareLocationTable.objects.all()
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


def software_update(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            software_id = json_data["software_id"]

            software_instance = SoftwareTable.objects.get(software_id=software_id)
            if software_instance == None:
                return JsonResponse({"status": "error", "message": "software not exist"})
            if "software_name" in json_data:
                software_instance.software_name = json_data["software_name"]
            if "software_version" in json_data:
                software_instance.software_version = json_data["software_version"]

            if "software_desc" in json_data:
                software_instance.software_desc = json_data["software_desc"]

            software_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

# 根据rsoftware_id 添加软件，同时根据rsoftwarelocation表中的信息部署到entity表中，后续补充
def software_add(request):
    if request.method == "POST":
        # json_data:  add_data:{"software_id":""}
        try:
            # json_data = request.POST.get("add_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            rsoftware_id = json_data["rsoftware_id"]
            rsoftware_instance = RegisterSoftwareTable.objects.get(
                rsoftware_id=rsoftware_id
            )
            if not rsoftware_instance:
                return JsonResponse(
                    {"status": "error", "message": "rsoftware_id not exist"}
                )
            software_instace = SoftwareTable()
            software_instace.software_id = rsoftware_id
            software_instace.software_version = rsoftware_instance.rsoftware_version
            software_instace.software_name = rsoftware_instance.rsoftware_name
            # 应该加上一个路经检测，后期加
            software_instace.software_hash = calculate_file_hash(rsoftware_instance.rsoftware_path)
            software_instace.software_desc = rsoftware_instance.rsoftware_desc
            software_instace.user_id = rsoftware_instance.user_id
            software_instace.save()
            """
            将rsoftwarelocation表中的信息部署到entity表中            
            """
            for rlsoftwarelocation_instance in RegisterSoftwareLocationTable.objects.filter(rsoftware_id=rsoftware_id):
                entity_instance = EnityTable()
                entity_instance.software_id = software_instace
                entity_instance.user_id = software_instace.user_id
                entity_instance.node_id = NodeTable.objects.get(node_ip=rlsoftwarelocation_instance.node_ip)
                entity_instance.entity_ip = rlsoftwarelocation_instance.entity_ip
                entity_instance.save()
            #删除rsoftwarelocation表和rsoftware中的信息 
            rsoftwarelocation_instace = RegisterSoftwareLocationTable.objects.filter(rsoftware_id=rsoftware_id)
            for rsoftwarelocation_instace in rsoftwarelocation_instace:
                rsoftwarelocation_instace.delete()
            rsoftware_instance.delete()

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def software_query_all(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = SoftwareTable.objects.all()
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

def software_query_by_id(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("query_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            software_id = json_data["software_id"]
            query_instance = SoftwareTable.objects.get(software_id=software_id)
            if not query_instance:
                return JsonResponse({"status": "error", "message": "software_id not exist"})
            data = query_instance.get_data()
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

# 删除software,同时需要撤销相关entity，后续补充
def software_delete(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("delete_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            software_id = json_data["software_id"]
            software_instance = SoftwareTable.objects.get(software_id=software_id)
            if not software_instance:
                return JsonResponse({"status": "error", "message": "software_id not exist"})
            """
            撤销已部署的相关实体
            """
            software_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def approve_software_register(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            rsoftware_id = json_data["rsoftware_id"]
            is_approve = json_data["is_approved"]
            if is_approve:
                rsoftware_instance = RegisterSoftwareTable.objects.get(rsoftware_id=rsoftware_id)
                software_instance = SoftwareTable()
                software_instance.software_id = rsoftware_instance.rsoftware_id
                software_instance.software_version = rsoftware_instance.rsoftware_version
                software_instance.software_name = rsoftware_instance.rsoftware_name
                # 应该加上一个路经检测，后期加

                software_instance.software_hash = calculate_file_hash(
                    rsoftware_instance.rsoftware_path
                )
                software_instance.software_desc = rsoftware_instance.rsoftware_desc
                software_instance.user_id = rsoftware_instance.user_id

                """
                将rsoftwarelocation表中的信息部署到entity表中            
                """
                for rlsoftwarelocation_instance in RegisterSoftwareLocationTable.objects.filter(rsoftware_id=rsoftware_id):
                    entity_instance = EnityTable()
                    node_instace = NodeTable.objects.get(
                        node_ip=rlsoftwarelocation_instance.node_ip
                    )
                    entity_instance.software_id = software_instance
                    entity_instance.user_id = software_instance.user_id
                    entity_instance.node_id = NodeTable.objects.get(
                        node_ip=rlsoftwarelocation_instance.node_ip
                    )
                    entity_instance.software_name = software_instance.software_name
                    entity_instance.entity_ip = rlsoftwarelocation_instance.entity_ip
                    entity_instance.entity_pid = utils.calculate_pid(
                        software_instance.software_hash,
                        rlsoftwarelocation_instance.entity_ip,
                    )
                    entity_instance.create_time = timezone.now()
                    entity_instance.update_time = timezone.now()
                    # 发送对应的ap，如果部署ap围在线就退出
                    payload = {
                        "add_data": {
                            "entity_pid": entity_instance.entity_pid,
                            "software_id": software_instance.software_id,
                            "software_hash": software_instance.software_hash,
                            "user_id": software_instance.user_id.user_id,
                            "entity_ip": rlsoftwarelocation_instance.entity_ip,
                        }
                    }
                    response = post_to_ap(
                        node_instace.node_ip,
                        node_instace.node_port,
                        "/entitymanage/addentity/",
                        payload=payload,
                    )
                    # print(response.json())
                    if response.json()["status"] == "success":
                        software_instance.save()
                        entity_instance.save()
                    else:
                        return JsonResponse(
                            {"status": "error", "message": response.json()["message"]}
                        )

                # 删除rsoftwarelocation表和rsoftware中的信息

                rsoftwarelocation_instace = RegisterSoftwareLocationTable.objects.filter(
                    rsoftware_id=rsoftware_id
                )
                for tmp_instace in rsoftwarelocation_instace:
                    tmp_instace.delete()
                rsoftware_instance.delete()
            else:
                rsoftware_instance = RegisterSoftwareTable.objects.get(rsoftware_id=rsoftware_id)
                rlsoftwarelocation_instance_list= RegisterSoftwareLocationTable.objects.filter(rsoftware_id=rsoftware_id)
                for rlsoftwarelocation_instance in rlsoftwarelocation_instance_list:
                    rlsoftwarelocation_instance.delete()

                rsoftware_instance.delete()
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
