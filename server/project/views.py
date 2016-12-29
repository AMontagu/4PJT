from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view

from server.customLogging import *

@api_view(['POST'])
def loginUser(request):
	print("ici login")
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			LOGINFO("login success with username " + username + "password " + password)
			return HttpResponse(status=200)
		else:
			email = username
			user = User.objects.get(email=email)
			if user is not None:
				user = authenticate(username=user.username, password=password)
				if user is not None:
					login(request, user)
					LOGINFO("login success with username " + username + "password " + password)
					return HttpResponse(status=200)
				else:
					LOGINFO("fail login with email " + email + "password " + password)
					return HttpResponse(status=400)
			else:
				LOGINFO("fail login with username/email " + username + " or password " + password)
				return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

@api_view(['POST'])
def signinUser(request):
	print("ici signin")
	if request.method == "POST":
		print(request.data)
		email = request.data['email']
		username = request.data['username']
		password = request.data['password']
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except Exception:
			LOGWARN("Sign in fail message :" + str(Exception))
			return HttpResponse("error create user", status=400, reason="error create user")
		return HttpResponse(status=200)

def logoutUser(request):
	logout(request)
