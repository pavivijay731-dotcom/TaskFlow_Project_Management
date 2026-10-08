from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def register(request):

    if request.method == "GET":
        return render(request, "accounts/register.html")

    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({
                "error": "Username and password are required"
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "error": "Username already exists"
            }, status=400)

        User.objects.create_user(
            username=username,
            password=password
        )

        return JsonResponse({
            "success": True,
            "message": "Registration successful"
        })

    return JsonResponse({
        "error": "Invalid request"
    }, status=405)


@csrf_exempt
def login(request):

    if request.method == "GET":
        return render(request, "accounts/login.html")

    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            return JsonResponse({
                "success": True,
                "message": "Login successful"
            })

        return JsonResponse({
            "success": False,
            "error": "Invalid username or password"
        }, status=401)

    return JsonResponse({
        "error": "Invalid request"
    }, status=405)