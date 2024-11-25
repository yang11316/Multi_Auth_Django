from django.urls import path
from . import views


urlpatterns = [path("get-dds-info", views.get_dds_info, name="get_dds_info")]
