from django.urls import path
from . import views

urlpatterns = [
    path("node-update/<str:pk>", views.node_update, name="node-update"),
]
