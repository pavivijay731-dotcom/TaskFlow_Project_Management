from django.urls import path
from . import views


urlpatterns = [

    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Project API
    path("api/", views.project_list, name="project_list"),

    # Task API
    path(
        "api/<int:project_id>/tasks/",
        views.task_list,
        name="task_list"
    ),

    # Update / Delete Task
    path(
        "api/tasks/<int:task_id>/",
        views.task_update,
        name="task_update"
    ),
]