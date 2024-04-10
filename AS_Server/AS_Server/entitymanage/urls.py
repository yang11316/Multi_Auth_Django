from django.urls import path
from . import views

urlpatterns = [
    path("addentity/", views.entity_add, name="entity-add"),
    path("getToken/", views.getToken, name="get-token"),
    path("queryentity/", views.entity_query, name="entity-query"),
    path(
        "calculateparticalkey/",
        views.entity_calculate_parcialkey,
        name="calculate-parcialkey",
    ),
    path("withdrawentity/", views.entity_withdraw, name="withdraw-entity"),
]
