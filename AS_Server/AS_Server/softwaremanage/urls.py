from django.urls import path
from . import views

urlpatterns = [
    path("registsoftware-add/", views.registsoftware_add, name="registsoftware-add"),
    path(
        "registsoftware-query-all/",
        views.registsoftware_query_all,
        name="registsoftware-query-all",
    ),
    path(
        "registsoftware-query-by-id/",
        views.registsoftware_query_by_id,
        name="registsoftware-query-by-id",
    ),
    path(
        "registsoftwarelocation-query-by-id/",
        views.registsoftwarelocation_query_by_id,
        name="registsoftwarelocation-query-by-id",
    ),
    path(
        "registsoftwarelocation-query-all/",
        views.registsoftwarelocation_query_all,
        name="registsoftwarelocation-query-all",
    ),
    path("software-add/", views.software_add, name="software_add"),
    path("software-query-all/", views.software_query_all, name="software_query_all"),
    path(
        "software-query-by-id/", views.software_query_by_id, name="software_query_by_id"
    ),
    path("software-delete/", views.software_delete, name="software_delete"),
    path(
        "approve-software-register/",
        views.approve_software_register,
        name="approve_software_register",
    ),
    path("update-software/", views.software_update, name="update_software"),
]
