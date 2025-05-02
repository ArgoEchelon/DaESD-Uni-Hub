from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>/', views.user_detail, name='user_detail'),
]