from django.urls import path, include

from work_stream import views

urlpatterns = [
    path('', views.get_all_projects, name="projects"),
    path('project/<str:project_id>/', views.get_project, name="project"),
    path('create-project/', views.create_project, name="create-project"),

    path('delete-project/<str:project_id>/',
         views.delete_project,
         name="delete-project"),

    path('update-project/<str:project_id>/',
         views.update_project,
         name="update-project"),

    path('tag/<slug:tag_slug>/',
         views.projects_by_tag,
         name="tag"),
]
