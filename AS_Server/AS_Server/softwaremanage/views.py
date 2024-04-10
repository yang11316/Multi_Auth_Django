from django.http import JsonResponse
from django.shortcuts import render
from commonutils.utils import *
from usermanage.models import *
from .models import *
import json


# Create your views here.


def registsoftware_add(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("add_data")
            json_data = json.loads(json_data)

            # 获取数据
            rsoftware_instace = RegisterTable()
            rsoftware_instace.rsoftware_name = json_data["rsoftware_name"]
            rsoftware_instace.rsoftware_path = json_data["rsoftware_path"]
            rsoftware_instace.rsoftware_version = json_data["rsoftware_version"]

            rsoftware_instace.node_ip = json_data["node_ip"]
            rsoftware_instace.pc_ip = json_data["pc_ip"]
            rsoftware_instace.rsoftware_desc = json_data["rsoftware_desc"]
            user_id = json_data["user_id"]
            user_instance = UserTable.objects.get(user_id=user_id)
            rsoftware_instace.user_id = user_instance
            rsoftware_instace.save()
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


def software_add(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("add_data")
            json_data = json.loads(json_data)
            rsoftware_path = json_data["rsoftware_path"]

            software_instace = SoftwareTable()
            software_instace.software_id = calculate_str_hash(
                json_data["software_name"] + json_data["software_version"]
            )
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
