from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from .models import ManagerTable, UserTable

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        path = [
            "/usermanage/user-login/",
            "/usermanage/user-register/",
            "/entitymanage/get-alive-entity/",
            "/entitymanage/get-down-entity/",
            "/entitymanage/calculate-particalkey/",
            "/entitymanage/get-public-parameter/",
            "/domainmanage/get-domain-key/",
            "/domainmanage/send-domain-key/",
            "/ddsmanage/get-dds-info/",
        ]
        if request.path not in path:
            try:
                if "token" in request.COOKIES:
                    token = request.COOKIES["token"]
                else:
                    token = request.headers["X-Token"]

                if UserTable.objects.get(user_id=token) == None:
                    return JsonResponse({"status": "error", "message": "not login"})

            except Exception as e:
                print(e)
                return JsonResponse({"status": "error", "message": "not login"})
