from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('community/<int:community_pk>/new/', views.event_create, name='event_create'),
    path('<int:pk>/join/', views.join_event, name='join_event'),
]