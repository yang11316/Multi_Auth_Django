from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import DomainTable
from entitymanage.models import KGCParamterTable
import json
import requests


# 接收ap发来的domain——key请求
def get_domain_key(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            if "domain_id" not in json_data:
                return JsonResponse(
                    {"status": "error", "message": "domain_id not found"}
                )
            domain_id = json_data["domain_id"]
            domain_instance = DomainTable.objects.filter(domain_id=domain_id).exists()
            if not domain_instance:
                return JsonResponse({"status": "error", "message": "domain not found"})
            domain_instance = DomainTable.objects.get(domain_id=domain_id)
            domain_ip = domain_instance.domain_ip
            domain_port = domain_instance.domain_port

            # 获取自身的domain id
            self_id = DomainTable.objects.get(domain_ip="0.0.0.0").domain_id

            payload = {"domain_id": self_id}
            response = post_to_domain_as(
                domain_ip,
                domain_port,
                "/domainmanage/send-domain-key/",
                payload=payload,
            )
            if response == None:
                return JsonResponse({"status": "error", "message": "domain not found"})
            if response.json()["status"] != "success":
                return JsonResponse({"status": "error"})
            print(response.json())
            return JsonResponse(response.json())

        except Exception as e:
            print(e)
            return HttpResponse({"status": "error", "message": str(e)})


# 接收其他as发来的domain——key请求
def send_domain_key(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            domain_id = json_data["domain_id"]
            domain_instance = DomainTable.objects.filter(domain_id=domain_id).exists()
            if not domain_instance:
                return JsonResponse({"status": "error", "message": "domain not found"})
            temp_params = KGCParamterTable.objects.get(kgc_id="kgc_id")
            kgc_Ppub = temp_params.kgc_Ppub
            acc_pub = temp_params.kgc_acc_publickey
            acc_cur = temp_params.kgc_acc_cur
            return JsonResponse(
                {
                    "status": "success",
                    "kgc_Ppub": kgc_Ppub,
                    "acc_pub": acc_pub,
                    "acc_cur": acc_cur,
                }
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 向其他AS发送http请求
def post_to_domain_as(node_ip: str, node_port: int, path: str, payload: dict):
    header = {"content-type": "application/json", "Connection": "close"}
    url = "http://" + node_ip + ":" + str(node_port) + path
    data = json.dumps(payload)
    try:
        res = requests.post(url, data=data, headers=header)
        return res
    except Exception as e:
        return {"status": "error"}
