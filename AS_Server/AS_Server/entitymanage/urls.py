from django.urls import path
from . import views

urlpatterns = [
    path("entity-query-alive/", views.entity_query_alive, name="entity-query-alive"),
    path("add-entity/", views.entity_add, name="entity-add"),
    # path("getToken/", views.getToken, name="get-token"),
    path("query-entity/", views.entity_query_pid, name="entity-query"),
    path("query-entity-all/", views.entity_query_all, name="entity-query-all"),
    path(
        "calculate-particalkey/",
        views.entity_calculate_parcialkey,
        name="calculate-parcialkey",
    ),
    path("withdraw-entity/", views.entity_withdraw, name="withdraw-entity"),
    path("get-alive-entity/", views.get_alive_entity_pid, name="get-alive-entity"),
    path("get-down-entity/", views.get_down_entity_pid, name="get-down-entity"),
]
