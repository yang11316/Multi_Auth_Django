from django.http import JsonResponse
from .models import NodeTable
import datetime, json
from commonutils.utils import *
from django.utils import timezone


# Create your views here.
def node_update(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("update_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            node_id = json_data["node_id"]
            update_instance = NodeTable.objects.get(node_id=node_id)
            if not update_instance:
                return JsonResponse({"status": "error", "message": "node not found"})
            # node_ip = json_data["node_ip"]
            # node_port = int(json_data["node_port"])
            node_desc = json_data["node_desc"]
            # update_instance.node_ip = node_ip
            # update_instance.node_port = node_port
            update_instance.node_desc = node_desc
            update_instance.update_time = timezone.now()
            update_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def node_add(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("add_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            node_ip = json_data["node_ip"]
            node_port = int(json_data["node_port"])
            node_desc = json_data["node_desc"]
            node_instance = NodeTable()
            node_instance.node_ip = node_ip
            node_instance.node_port = node_port
            if node_port < 0 or node_port > 65535:
                return JsonResponse({"status": "error", "message": "port out of range"})
            node_instance.node_desc = node_desc
            node_instance.node_id = calculate_str_hash(node_ip + node_port)
            node_instance.node_is_alive = True
            node_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def node_query_all(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]

            query_instance = NodeTable.objects.all()
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


def node_query_by_id(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("query_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            node_id = json_data["node_id"]
            node_instance = NodeTable.objects.get(node_id=node_id)
            if not node_instance:
                return JsonResponse({"status": "error", "message": "node not exist"})
            data = node_instance.get_data()
            return JsonResponse({"status": "success", "message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 同时还需撤销相关注册实体，后续补充
def node_delete(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("delete_data")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            node_id = json_data["node_id"]
            node_instance = NodeTable.objects.get(node_id=node_id)
            if not node_instance:
                return JsonResponse({"status": "error", "message": "node not exist"})
            """
            撤销实体
            """
            node_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
