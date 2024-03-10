from django.urls import path, include
from work_stream import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('project-object/<str:pk>/', views.project, name="project")
]
