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
            rsoftware_instace = RegisterTable()
            rsoftware_instace.rsoftware_id = calculate_str_hash(
                json_data["rsoftware_name"] + json_data["rsoftware_version"]
            )
            rsoftware_instace.rsoftware_name = json_data["rsoftware_name"]
            rsoftware_instace.rsoftware_path = json_data["rsoftware_path"]
            rsoftware_instace.rsoftware_version = json_data["rsoftware_version"]
            rsoftware_instace.rsoftware_desc = json_data["rsoftware_desc"]
            user_id = json_data["user_id"]
            user_instance = UserTable.objects.get(user_id=user_id)
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


def registsoftware_query(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            field = json_data.get("field")
            value = json_data.get("value")
            query_instance = RegisterTable.objects.filter(**{field: value})
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def registsoftwarelocation_query(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            field = json_data.get("field")
            value = json_data.get("value")
            query_instance = RegisterSoftwareLocationTable.objects.filter(
                **{field: value}
            )
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def registsoftwarelocation_query_all(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            field = json_data.get("field")
            value = json_data.get("value")
            query_instance = RegisterSoftwareLocationTable.objects.all()
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def software_add(request):
    if request.method == "POST":
        # json_data:  add_data:{"software_id":"","software_name":"","rsoftware_path":"","software_version":"","user_id":"","software_desc":""}
        try:
            json_data = request.POST.get("add_data")
            json_data = json.loads(json_data)
            rsoftware_path = json_data["rsoftware_path"]
            if SoftwareTable.objects.get(software_id=json_data["software_id"]):
                return JsonResponse(
                    {"status": "error", "message": "software_id already exist"}
                )
            software_instace = SoftwareTable()
            software_instace.software_id = json_data["software_id"]
            software_instace.software_version = json_data["software_version"]
            software_instace.software_name = json_data["software_name"]
            software_instace.software_hash = calculate_file_hash(rsoftware_path)
            software_instace.software_desc = json_data["software_desc"]
            user_id = json_data["user_id"]
            user_instace = UserTable.objects.get(user_id=user_id)
            software_instace.user_id = user_instace
            software_instace.save()
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def software_query(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("json_data")
            field = json_data.get("field")
            value = json_data.get("value")
            query_instance = RegisterTable.objects.filter(**{field: value})
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
