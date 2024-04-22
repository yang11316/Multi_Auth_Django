from django.http import JsonResponse
from django.shortcuts import render
from commonutils.utils import *
from usermanage.models import *
from .models import *
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
            json_data = request.POST.get("add_data")
            json_data = json.loads(json_data)

            # 获取数据
            rsoftware_instace = RegisterSoftwareTable()
            rsoftware_instace.rsoftware_id = calculate_str_hash(
                json_data["rsoftware_name"] + json_data["rsoftware_version"]
            )
            rsoftware_instace.rsoftware_name = json_data["rsoftware_name"]
            rsoftware_instace.rsoftware_path = json_data["rsoftware_path"]
            rsoftware_instace.rsoftware_version = json_data["rsoftware_version"]
            rsoftware_instace.rsoftware_desc = json_data["rsoftware_desc"]
            user_id = json_data["user_id"]
            user_instance = UserTable.objects.get(user_id=user_id)
            if(user_instance == None):
                return JsonResponse({"status": "add error failed", "message": "user not exist"})
            rsoftware_instace.user_id = user_instance
            rsoftware_instace.save()

            # 保存注册的location信息
            location_data = json_data["location_data"]
            for tmp in location_data:
                rsoftwarelocation_instace = RegisterSoftwareLocationTable()
                rsoftwarelocation_instace.rsoftware_id = rsoftware_instace
                rsoftwarelocation_instace.node_ip = tmp["node_ip"]
                rsoftwarelocation_instace.entity_ip = tmp["entity_ip"]
                rsoftwarelocation_instace.save()

        except Exception as e:
            return JsonResponse({"status": "add error failed", "message": str(e)})

def registsoftware_query_all(request):
    if request.method == "POST":
        try:
            query_instace = RegisterSoftwareTable.objects.all()
            data = {
                "num": query_instace.count(),
                "data": [temp.get_data() for temp in query_instace],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def registsoftware_query_by_id(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("query_data")
            json_data = json.loads(json_data)
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
            json_data = request.POST.get("query_data")
            json_data = json.loads(json_data)
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
            query_instance = RegisterSoftwareLocationTable.objects.all()
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

# registsoftware update 后续补充
"""
registsoftware_update:
"""

# 根据rsoftware_id 添加软件，同时根据rsoftwarelocation表中的信息部署到entity表中，后续补充
def software_add(request):
    if request.method == "POST":
        # json_data:  add_data:{"software_id":""}
        try:
            json_data = request.POST.get("add_data")
            json_data = json.loads(json_data)
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
            将rsoftwarelocation表中的信息部署到entity表中，后续补充
            
            """


            #删除rsoftwarelocation表和rsoftware中的信息 
            

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def software_query_all(request):
    if request.method == "POST":
        try:
            query_instance = SoftwareTable.objects.all()
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def software_query_by_id(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("query_data")
            json_data = json.loads(json_data)
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
            json_data = request.POST.get("delete_data")
            json_data = json.loads(json_data)
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

