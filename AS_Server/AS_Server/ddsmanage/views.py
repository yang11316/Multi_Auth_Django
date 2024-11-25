from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import DDSInfoTable
from entitymanage.models import EnityTable
import json
import requests

# Create your views here.


# 接收AP发来的实体的dds信息
def get_dds_info(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            entity_pid = json_data["entity_pid"]
            if not EnityTable.objects.filter(entity_pid=entity_pid).exists():
                return JsonResponse(
                    {"status": "error", "message": "entity_pid not exist"}
                )
            dds_type = json_data["dds_type"]
            source_ip = json_data["source_ip"]
            source_port = json_data["source_port"]
            destination_ip = json_data["destination_ip"]
            destination_port = json_data["destination_port"]
            DDSInstance = DDSInfoTable()
            DDSInstance.entity_pid = entity_pid
            DDSInstance.dds_type = dds_type
            DDSInstance.source_ip = source_ip
            DDSInstance.source_port = source_port
            DDSInstance.destination_ip = destination_ip
            DDSInstance.destination_port = destination_port
            DDSInstance.save()
            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
