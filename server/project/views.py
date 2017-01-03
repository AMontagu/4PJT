from datetime import datetime
from importlib import import_module

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import utc
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes

from project.models import QwirkUser
from server import settings
from server.customLogging import *


@api_view(['POST'])
def loginUser(request):
	print("ici login")
	if request.method == "POST":
		username = request.data['userName']
		password = request.data['password']
		user = authenticate(username=username, password=password)
		if user is None:
			email = username
			user = User.objects.get(email=email)
		if user is not None:
			user = authenticate(username=user.username, password=password)
			LOGINFO("login success with username " + username + " password " + password)
			if user is not None:
				token, created = Token.objects.get_or_create(user=user)
				if not created:
					# update the created time of the token to keep it valid
					token.created = datetime.utcnow().replace(tzinfo=utc)
					token.save()
				return HttpResponse(token.key, status=200)
			else:
				LOGINFO("fail login with username/email " + username + " password " + password)
				return HttpResponse(status=400)
		else:
			LOGINFO("fail login with username/email " + username + " password " + password)
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)


@api_view(['POST'])
def signinUser(request):
	print("ici signin")
	if request.method == "POST":
		print(request.data)
		email = request.data['email']
		username = request.data['userName']
		password = request.data['password']

		birthDate = None
		bio = None
		if 'birthDate' in request.data:
			birthDate = request.data['birthDate']
		if 'birthDate' in request.data:
			bio = request.data['bio']

		try:
			# User.objects.filter(username__iexact=username).exists()
			user = User.objects.create_user(username, email, password)
			user.save()
			qwirkUser = QwirkUser.objects.create(bio=bio, birthDate=birthDate, user=user)
			qwirkUser.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				LOGINFO("login success with username " + username + "password " + password)
				token = Token.objects.create(user=user)
				# update the created time of the token to keep it valid
				token.created = datetime.utcnow().replace(tzinfo=utc)
				token.save()
				return HttpResponse(token.key, status=200)
			else:
				LOGINFO("fail login with username/email " + username + " or password " + password)
				return HttpResponse(status=400)
		except Exception as e:
			LOGWARN("Sign in fail message :" + str(e))
			return HttpResponse("error create user", status=400, reason="error create user")


@api_view(['GET'])
def logoutUser(request):
	logout(request)


@api_view(['GET'])
def isLoggedIn(request):
	print(request.META)
	return HttpResponse(str(request.user.is_authenticated()), status=200)
