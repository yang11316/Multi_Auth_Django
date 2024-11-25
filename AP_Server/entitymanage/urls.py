from django.urls import path
from . import views

urlpatterns = [
    path("getentity/", views.get_entity, name="get-entity"),
    path("getauxdata/",views.get_aux_data,name="get-aux-data"),
    path("sendparticalkeyandpid/",views.send_particalkey_and_pid,name="send-particalkey-and-pid"),
    path("getdomainparameters/",views.get_domain_parameters,name="get-domain-parameters"),
    path("getddsinfo/",views.get_dds_info,name="get-dds-info")
]