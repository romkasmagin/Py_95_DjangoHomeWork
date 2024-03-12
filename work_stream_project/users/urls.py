from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('skill/<slug:skill_slug>', views.profiles_by_skill, name="skill"),
]
