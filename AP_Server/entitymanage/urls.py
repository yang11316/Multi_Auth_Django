from django.urls import path
from . import views

urlpatterns = [
    path("addentity/", views.get_entity_data, name="entity-add"),
    path("getparcialkey/", views.get_parcial_key, name="get-parcial-key"),
    path("getwithdrawdata/",views.get_withdraw_data,name="get-withdraw-data"),
    path("getauxdata/",views.get_aux_data,name="get-aux-data"),
    path("sendparticalkeyandpid/",views.send_particalkey_and_pid,name="send-particalkey-and-pid"),
    
]