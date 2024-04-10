from django.urls import path
from . import views

urlpatterns  = [
    path('user-register/', views.user_register, name='user-register'),
    path('approve-register/<str:pk>', views.approve_register, name='approve-register'),
    path('delete-user/<str:pk>',views.user_delete,name="delete-user"),
    path('user-update/<str:pk>',views.user_update,name="user-update"),
    path('get-user/<str:pk>',views.user_query,name="get-user"),
    path('user-query',views.user_query,name="user-query"),
    ]

