from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Project, Task
import json


# Dashboard
def dashboard(request):
    return render(request, "projects/index.html")


# Project API
@csrf_exempt
def project_list(request):

    if request.method == "GET":

        projects = Project.objects.all().order_by("-created_at")

        data = []

        for project in projects:

            data.append({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_by": project.created_by.username,
                "created_at": project.created_at.strftime("%Y-%m-%d")
            })

        return JsonResponse(data, safe=False)


    if request.method == "POST":

        try:
            body = json.loads(request.body)

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)


        name = body.get("name")
        description = body.get("description", "")


        if not name:
            return JsonResponse({
                "error": "Project name is required"
            }, status=400)


        # Use currently logged-in user
        if not request.user.is_authenticated:
            return JsonResponse({
                "error": "Please login first"
            }, status=401)


        project = Project.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )


        return JsonResponse({
            "success": True,
            "message": "Project created successfully",
            "id": project.id
        })


    return JsonResponse({
        "error": "Invalid request"
    }, status=405)


# Task API
@csrf_exempt
def task_list(request, project_id):

    try:
        project = Project.objects.get(id=project_id)

    except Project.DoesNotExist:
        return JsonResponse({
            "error": "Project not found"
        }, status=404)


    if request.method == "GET":

        tasks = Task.objects.filter(
            project=project
        ).order_by("-created_at")

        data = []

        for task in tasks:

            data.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "due_date": task.due_date,
                "assigned_to": (
                    task.assigned_to.username
                    if task.assigned_to
                    else None
                )
            })

        return JsonResponse(data, safe=False)


    if request.method == "POST":

        try:
            body = json.loads(request.body)

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)


        title = body.get("title")
        description = body.get("description", "")
        status = body.get("status", "todo")


        if not title:
            return JsonResponse({
                "error": "Task title is required"
            }, status=400)


        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status
        )


        return JsonResponse({
            "success": True,
            "message": "Task created successfully",
            "id": task.id
        })


    return JsonResponse({
        "error": "Invalid request"
    }, status=405)


# Update / Delete Task
@csrf_exempt
def task_update(request, task_id):

    try:
        task = Task.objects.get(id=task_id)

    except Task.DoesNotExist:
        return JsonResponse({
            "error": "Task not found"
        }, status=404)


    if request.method == "PUT":

        try:
            body = json.loads(request.body)

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)


        task.title = body.get(
            "title",
            task.title
        )

        task.description = body.get(
            "description",
            task.description
        )

        task.status = body.get(
            "status",
            task.status
        )

        task.save()


        return JsonResponse({
            "success": True,
            "message": "Task updated successfully"
        })


    if request.method == "DELETE":

        task.delete()

        return JsonResponse({
            "success": True,
            "message": "Task deleted successfully"
        })


    return JsonResponse({
        "error": "Invalid request"
    }, status=405)