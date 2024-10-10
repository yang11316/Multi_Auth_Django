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
        if (
            request.path != "/usermanage/user-login/"
            and request.path != "/usermanage/user-register/"
            and request.path != "/entitymanage/get-alive-entity/"
            and request.path != "/entitymanage/get-down-entity/"
        ):
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
