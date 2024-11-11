from django.urls import path
from . import views

urlpatterns = [
    path("get-domain-key/", views.get_domain_key, name="get-domain-key"),
    path("send-domain-key/", views.send_domain_key, name="send-domain-key"),
]
