from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  
    path('community/<int:community_pk>/', views.post_list, name='community_post_list'), 
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('new/<int:community_id>/', views.post_create, name='post_create'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
]