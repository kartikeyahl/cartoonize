from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render
from .models import UserImages
from io import BytesIO
from PIL import Image
import numpy as np         # importing numpy(to solve mathematical expressions)
import cv2                 # importing opencv library (image recog., image preprocessing)
import json

@csrf_exempt
def UserCreate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(username=data["username"],first_name=data["first_name"],
            last_name=data["last_name"],password=data["password"],email=data["email"])
        user.set_password(data["password"])
        return JsonResponse(user.username,safe=False)


@csrf_exempt
def UserLogin(request):
    if request.user.is_authenticated:
        data = "already logged in"
        return JsonResponse(data,safe=False)
    if request.method == "GET":
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            data = serialize("json",[user])
            return JsonResponse(json.loads(data),safe=False)
        else:
            data = "invalid credentials , please type your username and password correctly"
            return JsonResponse(data,safe=False)

def logout_view(request):
    logout(request)
    return JsonResponse("Logged out",safe=False)

def Profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        data = {'user':user.username,'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'last_login':user.last_login}
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse("User is not logged in ",safe=False)

@csrf_exempt
def UploadImage(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            user = request.user
            image = request.FILES['image']
            image_data = UserImages.objects.create(user=user, image=image)
            image_data.saveCImage()
            data = {'uploaded_url':image_data.image.url,'cartoonized_image':image_data.cartoon_image.url}
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse("Unable to upload your image",safe=False)

def AllImages(request):
    if request.user.is_authenticated:
        user = request.user
        images = UserImages.objects.filter(user=user)
        data = serialize("json",images)
        return JsonResponse(json.loads(data),safe=False)
    else:
        return JsonResponse("Required Login",safe=False)