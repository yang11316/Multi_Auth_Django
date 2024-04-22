from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json, datetime
from .models import RegisterTable, UserTable
from commonutils.utils import *


# Create your views here.
def index(request):
    return HttpResponse("page sucess")


def user_register(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("register_form")
            json_data = json.loads(json_data)
            register_instance = RegisterTable()
            for key, value in json_data.items():
                setattr(register_instance, key, value)
            register_instance.create_time = datetime.now()
            register_instance.update_time = datetime.now()
            register_instance.user_id = calculate_str_hash(
                json_data["user_name"] + json_data["user_phone"] + str(datetime.now())
            )
            register_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def approve_register(request, pk):
    if request.method == "POST":
        try:
            approve_instance = RegisterTable.objects.get(user_id=pk)
            user_instance = UserTable()

            for field in RegisterTable._meta.fields:
                setattr(
                    user_instance, field.name, getattr(approve_instance, field.name)
                )

            user_instance.create_time = datetime.now()
            user_instance.create_time = datetime.now()
            user_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 删除用户，同时也要撤销用户注册的实体，后续补充
def user_delete(request):
    if request.method == "POST":
        json_data = request.get("delete_id")
        json_data = json.loads(json_data)
        user_id = json_data["user_id"]
        user_instance = UserTable.objects.get(user_id=user_id)
        try:
            user_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def user_update(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("update_form")
            json_data = json.loads(json_data)
            user_id = json_data["user_id"]
            update_instance = UserTable.objects.get(user_id=user_id)
            if update_instance != None:
                for key, value in json_data.items():
                    setattr(update_instance, key, value)
                update_instance.update_time = datetime.now()
                update_instance.save()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "user not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def user_query_all(request):
    if request.method == "POST":
        try:

            query_instance = UserTable.objects.all()
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def user_query_by_id(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("query_data")
            json_data = json.loads(json_data)
            user_id = json_data["user_id"]
            query_instance = UserTable.objects.filter(user_id=user_id)
            data = query_instance.get_data()
            return JsonResponse({"status": "success", "message": data})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
