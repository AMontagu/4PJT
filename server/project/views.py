from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from server.customLogging import *


def loginUser(request):
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

def signinUser(request):
	if request.method == "POST":
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except Exception:
			LOGWARN("Sign in fail message :" + str(Exception))
			return HttpResponse(status=400)
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=400)

def logoutUser(request):
	logout(request)
