from django.urls import path
from . import views

urlpatterns = [
    path('community/<int:community_pk>/', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('community/<int:community_pk>/new/', views.post_create, name='post_create'),
]