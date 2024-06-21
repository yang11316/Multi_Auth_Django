from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import RegisterTable, UserTable
from commonutils.utils import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, get_token


def send_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse(data={"token": csrf_token})


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("login_form")
            print(request.META.get("REMOTE_ADDR"))
            json_data = json.loads(request.body.decode("utf-8"))
            user_name = json_data["username"]
            user_pwd = json_data["password"]
            user_instance = UserTable.objects.get(user_name=user_name)
            print(user_name)
            if user_instance == None:
                return JsonResponse({"status": "error", "message": "用户不存在"})
            if user_instance.user_pwd != user_pwd:
                return JsonResponse({"status": "error", "message": "密码错误"})
            else:
                user_id = user_instance.user_id
                # csrf_token = get_token(request)
                user_role = user_instance.user_row
                if user_role == "admin":
                    payload = {"token": user_id}
                else:
                    payload = {"token": user_id}
                return JsonResponse({"status": "success", "data": payload})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def user_register(request):
    if request.method == "POST":
        try:
            # json_data = request.POST.get("register_form")
            # json_data = json.loads(json_data)
            json_data = json.loads(request.body.decode("utf-8"))
            print(json_data)
            register_instance = RegisterTable()
            register_instance.user_name = json_data["user_name"]
            register_instance.user_pwd = json_data["user_pwd"]
            if "user_phone" in json_data:
                register_instance.user_phone = json_data["user_phone"]
            if "user_email" in json_data:
                register_instance.user_email = json_data["user_email"]
            register_instance.create_time = timezone.now()
            register_instance.update_time = register_instance.create_time
            register_instance.user_id = calculate_str_hash(
                json_data["user_name"] + json_data["user_pwd"] + str(timezone.now())
            )
            register_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


def user_register_query_all(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = RegisterTable.objects.all()
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


def approve_register(request):
    if request.method == "POST":
        try:

            json_data = json.loads(request.body.decode("utf-8"))
            user_id = json_data["user_id"]
            approve_bool = json_data["is_approved"]
            print(approve_bool)
            if approve_bool:
                approve_instance = RegisterTable.objects.get(user_id=user_id)
                user_instance = UserTable()

                user_instance.user_id = user_id
                user_instance.user_name = approve_instance.user_name
                user_instance.user_pwd = approve_instance.user_pwd
                user_instance.user_phone = approve_instance.user_phone
                user_instance.user_email = approve_instance.user_email

                user_instance.create_time = timezone.now()
                user_instance.update_time = user_instance.create_time
                user_instance.save()
                approve_instance.delete()

            else:
                approve_instance = RegisterTable.objects.get(user_id=user_id)
                approve_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 删除用户，同时也要撤销用户注册的实体，后续补充
# delete_id:{"user_id":"aaaaa"}


# data   =   delete_id:{"user_id":"aaaaa"}
def user_delete(request):
    if request.method == "POST":
        # json_data = request.get("delete_id")
        json_data = json.loads(request.body.decode("utf-8"))
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
            json_data = json.loads(request.body.decode("utf-8"))
            print(json_data)
            user_id = json_data["user_id"]
            update_instance = UserTable.objects.get(user_id=user_id)
            if update_instance != None:
                if "user_email" in json_data:
                    update_instance.user_email = json_data["user_email"]
                if "user_phone" in json_data:
                    update_instance.user_phone = json_data["user_phone"]
                if "user_name" in json_data:
                    update_instance.user_name = json_data["user_name"]
                if "user_row" in json_data:
                    update_instance.user_row = json_data["user_row"]

                update_instance.update_time = timezone.now()
                update_instance.save()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "user not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def user_info(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            user_id = json_data["user_id"]
            print(user_id)
            user_instance = UserTable.objects.get(user_id=user_id)
            if user_instance == None:
                return JsonResponse({"status": "success", "message": "user not exist"})
            csrf_token = get_token(request)
            user_role = user_instance.user_row
            if user_role == "admin":
                payload = {
                    "roles": [user_role],
                    "introduction": "I am a super administrator",
                    "avatar": "https://upload.shejihz.com/2019/03/fe2ec2e7ed7f6795b46b793d93c99b7e.jpg",
                    "name": "管理员",
                    # "csrf_token": csrf_token,
                }
            else:
                payload = {
                    "roles": [user_role],
                    "introduction": "I am an editor",
                    "avatar": "https://upload.shejihz.com/2019/03/fe2ec2e7ed7f6795b46b793d93c99b7e.jpg",
                    "name": "软件开发人员",
                    # "csrf_token": csrf_token,
                }
            return JsonResponse({"status": "success", "data": payload})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def logout(request):
    if request.method == "POST":
        return JsonResponse({"status": "success"})


def user_query_all(request):
    if request.method == "POST":
        try:
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)
            page = json_data["page"]
            limit = json_data["limit"]
            query_instance = UserTable.objects.all()
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
