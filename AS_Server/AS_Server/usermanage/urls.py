from django.urls import path
from . import views

urlpatterns = [
    path("user-register/", views.user_register, name="user-register"),
    path("approve-register/", views.approve_register, name="approve-register"),
    path("delete-user/", views.user_delete, name="delete-user"),
    path("user-update/", views.user_update, name="user-update"),
    path("get-user/", views.user_query_by_id, name="get-user"),
    path("user-query-all/", views.user_query_all, name="user-query"),
    path("user-login/", views.user_login, name="user-login"),
    path("user-info/", views.user_info, name="user-info"),
    path("user-logout/", views.logout, name="logout"),
    path(
        "registered-user-query-all/",
        views.user_register_query_all,
        name="registered-user-query-all",
    ),
]
