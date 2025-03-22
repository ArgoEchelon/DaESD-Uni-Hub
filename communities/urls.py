from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('<int:pk>/', views.community_detail, name='community_detail'),
    path('new/', views.community_create, name='community_create'),
    path('<int:pk>/join/', views.join_community, name='join_community'),
    path('<int:pk>/delete/', views.community_delete, name='community_delete'),
    path('<int:pk>/edit/', views.community_edit, name='community_edit'),
]