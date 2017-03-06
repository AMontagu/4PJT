from datetime import datetime
from importlib import import_module

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import utc
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer

from project.models import QwirkUser, Contact, QwirkGroup
from project.serializer import QwirkUserSerializer, QwirkUserSerializerSimple, QwirkGroupSerializer
from server import settings
from server.customLogging import *


@api_view(['POST'])
def loginUser(request):
	print("ici login")
	if request.method == "POST":
		username = request.data['username']
		password = request.data['password']
		user = authenticate(username=username, password=password)
		if user is None and User.objects.filter(email=username):
			user = User.objects.get(email=username)
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
		email = request.data['user']['email']
		username = request.data['user']['username']
		password = request.data['user']['password']
		lastname = request.data['user']['last_name']
		firstname = request.data['user']['first_name']

		birthDate = None
		bio = None
		if 'birthDate' in request.data and request.data['birthDate'] != "":
			birthDate = request.data['birthDate']
		if 'birthDate' in request.data:
			bio = request.data['bio']

		try:
			# User.objects.filter(username__iexact=username).exists()
			user = User.objects.create_user(username, email, password)
			user.first_name = firstname
			user.last_name = lastname
			user.save()
			qwirkUser = QwirkUser.objects.create(bio=bio, birthDate=birthDate, user=user, status="Online")
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


@api_view(['POST'])
def editUser(request):
	print("ici edit user")
	if request.user is not None:
		# TODO useless delete this
		if request.method == "POST":
			print(request.data)
			email = request.data['user']['email']
			lastname = request.data['user']['last_name']
			firstname = request.data['user']['first_name']

			print("lastname = " + lastname)
			print("firstname = " + firstname)

			birthDate = None
			bio = None
			if 'birthDate' in request.data and request.data['birthDate'] != "":
				birthDate = request.data['birthDate']
			if 'birthDate' in request.data:
				bio = request.data['bio']

			try:
				user = request.user
				user.first_name = firstname
				user.last_name = lastname
				user.email = email
				user.save()
				print(user)
				"""qwirkUser = request.user.qwirkuser
				qwirkUser.bio = bio
				qwirkUser.birthDate = birthDate
				qwirkUser.save()"""
			except Exception as e:
				LOGWARN("edit fail message :" + str(e))
				return HttpResponse("error create user", status=400, reason="error edit user")
			return HttpResponse(status=200)
	else:
		return HttpResponse(status=401)


@api_view(['GET'])
def logoutUser(request):
	logout(request)


@api_view(['GET'])
def isLoggedIn(request):
	return HttpResponse(str(request.user.is_authenticated()), status=200)

@api_view(['POST'])
def addContact(request):
	if request.user is not None:
		username = request.data['username']
		userContact = User.objects.get(username=username)
		if userContact is None:
			email = username
			userContact = User.objects.get(email=email)
		if userContact is not None:
			if request.user.qwirkuser.contacts.filter(qwirkUser=userContact.qwirkuser).exists():
				print("user have already this user as contact")
				return HttpResponse("Already in contact", status=200)
			else:
				qwirkGroup = QwirkGroup(name=userContact.username+"-"+request.user.username, private=True, isContactGroup=True)
				qwirkGroup.save()
				qwirkGroup.admin.add(request.user.qwirkuser)
				qwirkGroup.admin.add(userContact.qwirkuser)

				newContact = Contact.objects.create(qwirkUser=userContact.qwirkuser, status="Asking", qwirkGroup=qwirkGroup)
				newContact.save()
				newContact2 = Contact.objects.create(qwirkUser=request.user.qwirkuser, status="Pending", qwirkGroup=qwirkGroup)
				newContact2.save()
				request.user.qwirkuser.contacts.add(newContact)
				userContact.qwirkuser.contacts.add(newContact2)
				print("added " + newContact.qwirkUser.user.username)
				return HttpResponse(qwirkGroup.name, status=200)
		else:
			LOGINFO("No contact with this username/email " + username)
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=401)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def getUserInformations(request):
	if request.user is not None:
		"""for field in request.user._meta.fields:
			print(field.name)"""
		#qwirkUser = QwirkUser.objects.get(user=request.user)
		serializer = QwirkUserSerializer(request.user.qwirkuser)
		json = JSONRenderer().render(serializer.data)
		print(json)
		return HttpResponse(json, status=200)
	else:
		return HttpResponse(status=401)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def getSimpleUserInformations(request):
	if request.user is not None:
		"""for field in request.user._meta.fields:
			print(field.name)"""
		#qwirkUser = QwirkUser.objects.get(user=request.user)
		serializer = QwirkUserSerializerSimple(request.user.qwirkuser)
		json = JSONRenderer().render(serializer.data)
		#print(json)
		return HttpResponse(json, status=200)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
def createGroup(request):
	if request.user is not None:
		groupName = request.data['groupName']
		private = request.data['isPrivate']

		qwirkGroup = QwirkGroup(name=groupName, private=private, isContactGroup=False)
		qwirkGroup.save()
		qwirkGroup.admin.add(request.user.qwirkuser)

		serializer = QwirkGroupSerializer(qwirkGroup)
		print(JSONRenderer().render(serializer.data))

		request.user.qwirkuser.qwirkGroups.add(qwirkGroup)

		print(request.user.qwirkuser.qwirkGroups)


		return HttpResponse(status=201)
	else:
		return HttpResponse(status=401)
