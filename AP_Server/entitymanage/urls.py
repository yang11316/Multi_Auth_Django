from django.urls import path
from . import views

urlpatterns = [
    path("getentity/", views.get_entity, name="get-entity"),
    path("getauxdata/",views.get_aux_data,name="get-aux-data"),
    path("sendparticalkeyandpid/",views.send_particalkey_and_pid,name="send-particalkey-and-pid"),
    path("getopenport/",views.get_open_port,name="get-open-port"),
    
]