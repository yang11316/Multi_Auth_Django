from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json, datetime
from .models import RegisterTable, UserTable


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


def user_delete(request, pk):
    user_instance = UserTable.objects.get(user_id=pk)
    if request.method == "POST":
        try:
            user_instance.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def user_update(request, pk):
    if request.method == "POST":
        try:
            json_data = request.POST.get("update_form")
            json_data = json.loads(json_data)
            update_instance = UserTable.objects.get(user_id=pk)
            for key, value in json_data.items():
                setattr(update_instance, key, value)
            update_instance.update_time = datetime.now()
            update_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

def user_query(request):
    if request.method == "POST":
        try:
            json_data = request.POST.get("query_data")
            json_data = json.loads(json_data)
            field = json_data.get("field")
            value = json_data.get("value")
            query_instance = UserTable.objects.filter(**{field: value})
            data = {
                "num": query_instance.count(),
                "data": [temp.get_data() for temp in query_instance],
            }
            return JsonResponse({"status": "success", "message": data})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
def get_user(request, pk):
    if request.method == "POST":
        try:
            query_instance = UserTable.objects.get(user_id=pk)
            data = {
                "user_id": query_instance.user_id,
                "user_name": query_instance.user_name,
                "user_row": query_instance.user_row,
                "user_pwd": query_instance.user_pwd,
                "user_phone": query_instance.user_phone,
                "user_email": query_instance.user_email,
                "create_time": query_instance.create_time,
                "update_time": query_instance.update_time,
            }
            json_data = json.dumps(data)
            if json_data:
                return JsonResponse({"status": "success", "message": json_data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
