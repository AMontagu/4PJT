import mimetypes
from datetime import datetime
from importlib import import_module
from wsgiref.util import FileWrapper

from channels import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import utc
from os import path
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes, \
	parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer

from project import utils
from project.models import QwirkUser, Contact, QwirkGroup, Notification, Message
from project.serializer import QwirkUserSerializer, QwirkUserSerializerSimple, QwirkGroupSerializer, \
	NotificationSerializer, ContactSerializer, NotificationSerializerSimple, MessageSerializer
from server import settings
from server.customLogging import *
import json

from django.utils.encoding import smart_str


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
				login(request, user)
				print(request)
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
		# TODO check username for special charactere
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
		# textMessage = request.data['textMessage']
		textMessage = "Would you be my friend ?"
		userContact = User.objects.get(username=username)
		if userContact is None:
			email = username
			userContact = User.objects.get(email=email)
		if userContact is not None:
			if userContact != request.user:
				if request.user.qwirkuser.contacts.filter(qwirkUser=userContact.qwirkuser).exists():
					contact = request.user.qwirkuser.contacts.get(qwirkUser=userContact.qwirkuser)
					contactAsked = userContact.qwirkuser.contacts.get(qwirkUser=request.user.qwirkuser)
					print("user have already this user as contact")
					if contact.status == "Block" or contact.status == "Block":
						print("user blocked")
						jsonResponse = JSONRenderer().render(
							{'status': 'error', 'name': 'UserBlocked', 'text': 'This user is bocked'})
						return HttpResponse(jsonResponse, status=403)
					contact.status = "Asking"
					contact.save()
					contactAsked.status = "Pending"
					contactAsked.save()

					qwirkGroup = QwirkGroup.objects.get(name=userContact.username+"-"+request.user.username)
				else:
					qwirkGroup = QwirkGroup(name=userContact.username+"-"+request.user.username, isPrivate=True, isContactGroup=True)
					qwirkGroup.save()
					qwirkGroup.admins.add(request.user.qwirkuser)
					qwirkGroup.admins.add(userContact.qwirkuser)

					contact = Contact.objects.create(qwirkUser=userContact.qwirkuser, status="Asking", qwirkGroup=qwirkGroup)
					contact.save()
					contactAsked = Contact.objects.create(qwirkUser=request.user.qwirkuser, status="Pending", qwirkGroup=qwirkGroup)
					contactAsked.save()
					request.user.qwirkuser.contacts.add(contact)
					userContact.qwirkuser.contacts.add(contactAsked)
					print("added " + contact.qwirkUser.user.username)

				contactSerializer = ContactSerializer(contactAsked)

				text = json.dumps({
					"action": "newDemand",
					"contact": contactSerializer.data
				})
				Group("user" + userContact.username).send({
					"text": text,
				})

				utils.sendMessageToContact(userContact, qwirkGroup, request.user, textMessage, "requestMessage")

				serializer = ContactSerializer(contact)
				jsonResponse = JSONRenderer().render(serializer.data)
				return HttpResponse(jsonResponse, status=200)
			else:
				jsonResponse = JSONRenderer().render(
					{'status': 'error', "name": "AddingYourSelf", "message": "You can add yourself as contact"})
				return HttpResponse(jsonResponse, status=404)
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

		jsonResponse = JSONRenderer().render(serializer.data)
		# print(serializer.data['notifications'])
		return HttpResponse(jsonResponse, status=200)
	else:
		return HttpResponse(status=401)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def getSimpleUserInformations(request):
	if request.user is not None:

		username = request.GET.get('username', None)

		if username is None:
			serializer = QwirkUserSerializerSimple(request.user.qwirkuser)
		else:
			qwirkUser = QwirkUser.objects.get(user__username=username)
			serializer = QwirkUserSerializerSimple(qwirkUser)
		jsonResponse = JSONRenderer().render(serializer.data)
		return HttpResponse(jsonResponse, status=200)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def createGroup(request):
	if request.user is not None:
		groupName = request.data['groupName']
		isPrivate = request.data['isPrivate']

		if not QwirkGroup.objects.filter(name=groupName).exists():

			qwirkGroup = QwirkGroup(name=groupName, isPrivate=isPrivate, isContactGroup=False)
			qwirkGroup.save()
			qwirkGroup.admins.add(request.user.qwirkuser)

			request.user.qwirkuser.qwirkGroups.add(qwirkGroup)

			serializer = QwirkGroupSerializer(qwirkGroup)

			jsonResponse = JSONRenderer().render(serializer.data)

			return HttpResponse(jsonResponse, status=201)

		else:
			jsonResponse = JSONRenderer().render({'status': 'error', "name": "NameAlreadyExist", "message": "A group with this name already exist"})
			return HttpResponse(jsonResponse, status=404)
	else:
		return HttpResponse(status=401)

@api_view(['POST'])
def removeGroup(request):
	if request.user is not None:
		groupName = request.data['groupName']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		text = json.dumps({
			"action": "removeGroup",
			"groupName": groupName,
			"isContactGroup": qwirkGroup.isContactGroup
		})

		utils.sendCommandToAllUserGroup(qwirkGroup, request.user, text)

		qwirkGroup.delete()

		return HttpResponse(status=204)
	else:
		return HttpResponse(status=401)

@api_view(['POST'])
def quitGroup(request):
	if request.user is not None:
		groupName = request.data['groupName']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		if request.user.qwirkuser in qwirkGroup.admins.all():
			qwirkGroup.admins.remove(request.user.qwirkuser)
			if len(qwirkGroup.admins.all()) <= 0:
				# qwirkUserDefaultAdmin = QwirkUser.objects.filter(qwirkGroup=qwirkGroup).latest()
				try:
					qwirkUserDefaultAdmin = qwirkGroup.qwirkuser_set.earliest('id')
					qwirkGroup.admins.add(qwirkUserDefaultAdmin)
					utils.sendMessageToAllUserGroup(qwirkGroup, request.user, "new administrator: " + qwirkUserDefaultAdmin.user.username, "informations")
				except ObjectDoesNotExist:
					qwirkGroup.delete()

		groupOrChannel = "channel"
		if qwirkGroup.isPrivate:
			groupOrChannel = "group"
		utils.sendMessageToAllUserGroup(qwirkGroup, request.user, request.user.username + " leave this " + groupOrChannel, "informations")

		textUserLeave = json.dumps({
			"action": "userLeave",
			"username": request.user.username
		})
		utils.sendToQwirkGroup(qwirkGroup, request.user, textUserLeave)

		request.user.qwirkuser.qwirkGroups.remove(qwirkGroup)

		return HttpResponse(status=204)
	else:
		return HttpResponse(status=401)

@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def addUserToGroup(request):
	if request.user is not None:
		print(request.data)
		groupName = request.data['groupName']
		userName = request.data['username']
		isAdmin = request.data['isAdmin']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)
		userToAdd = User.objects.get(username=userName)

		if qwirkGroup in request.user.qwirkuser.qwirkGroups.all():
			if userToAdd.qwirkuser not in qwirkGroup.blockedUsers.all():
				if userToAdd.qwirkuser not in qwirkGroup.qwirkuser_set.all():
					userToAdd.qwirkuser.qwirkGroups.add(qwirkGroup)
					if isAdmin:
						qwirkGroup.admins.add(userToAdd)

					groupOrChannel = "channel"
					if qwirkGroup.isPrivate:
						groupOrChannel = "group"

					qwirkGroupSerializer = QwirkGroupSerializer(qwirkGroup)

					text = json.dumps({
						"action": "newGroup",
						"qwirkGroup": qwirkGroupSerializer.data,
					})
					Group("user" + userName).send({
						"text": text,
					})

					textMessage = request.user.username + " has invited " + userToAdd.username + " to join the " + groupOrChannel

					utils.sendMessageToAllUserGroup(qwirkGroup, request.user, textMessage, "informations")

					qwirkUserSerializer = QwirkUserSerializer(userToAdd.qwirkuser)

					textNewUser = json.dumps({
						"action": "newUser",
						"qwirkUser": qwirkUserSerializer.data
					})

					utils.sendToQwirkGroup(qwirkGroup, request.user, textNewUser)

					qwirkUserSerializer = QwirkUserSerializer(userToAdd.qwirkuser)

					jsonResponse = JSONRenderer().render({'status': 'success', 'qwirkUser': qwirkUserSerializer.data})
					return HttpResponse(jsonResponse, status=200)
				else:
					jsonResponse = JSONRenderer().render(
						{'status': 'error', 'name': 'UserAlreadyInGroup', 'message': 'This user is already in this group'})
					return HttpResponse(jsonResponse, status=400)
			else:
				print("user blocked")
				jsonResponse = JSONRenderer().render(
					{'status': 'error', 'name': 'UserBlocked', 'message': 'This user is bocked for this group'})
				return HttpResponse(jsonResponse, status=403)
		else:
			print("user not authorized to add someone")
			jsonResponse = JSONRenderer().render({'status': 'error', "name": "NoAdminRight", 'message': 'You need to be admin for add an user to the group'})
			return HttpResponse(jsonResponse, status=403)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def joinChannel(request):
	if request.user is not None:
		print(request.data)
		channelName = request.data['channelName']
		userName = request.data['username']

		qwirkGroup = QwirkGroup.objects.get(name=channelName)
		userToAdd = User.objects.get(username=userName)

		if userToAdd.qwirkuser not in qwirkGroup.blockedUsers.all():
			userToAdd.qwirkuser.qwirkGroups.add(qwirkGroup)

			serializer = QwirkGroupSerializer(qwirkGroup)

			jsonResponse = JSONRenderer().render({'status': 'success', 'qwirkGroup': serializer.data})
			return HttpResponse(jsonResponse, status=200)
		else:
			print("user blocked")
			jsonResponse = JSONRenderer().render(
				{'status': 'error', "name": "UserBlocked", 'message': 'This user is bocked for this group'})
			return HttpResponse(jsonResponse, status=403)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
def checkFriendship(request):
	if request.user is not None:

		friendName = request.data['username']

		if request.user.qwirkuser.contacts.filter(qwirkUser__user__username=friendName).exists():

			contact = request.user.qwirkuser.contacts.get(qwirkUser__user__username=friendName)

			if contact.status == "Friend":
				groupName = contact.qwirkGroup.name

				jsonResponse = JSONRenderer().render({'isFriend': True, 'groupName': groupName})
				return HttpResponse(jsonResponse, status=200)
			else:
				jsonResponse = JSONRenderer().render({'isFriend': False})
				return HttpResponse(jsonResponse, status=200)
		else:
			jsonResponse = JSONRenderer().render({'isFriend': False})
			return HttpResponse(jsonResponse, status=200)
	else:
		return HttpResponse(status=401)

@api_view(['POST'])
def giveAdminRight(request):
	if request.user is not None:
		groupName = request.data['groupName']
		newAdminUserName = request.data['username']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		if request.user.qwirkuser in qwirkGroup.admins.all():
			newAdmin = QwirkUser.objects.get(user__username=newAdminUserName)
			qwirkGroup.admins.add(newAdmin)

			return HttpResponse(status=200)
		else:
			jsonResponse = JSONRenderer().render({'status': 'error', "name": "NoAdminRight", 'message': 'You need to be admin for add admin right to user'})
			return HttpResponse(jsonResponse, status=403)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
def blockUser(request):

	if request.user is not None:
		groupName = request.data['groupName']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		for contact in qwirkGroup.contact_set.all():
			contact.status = "Block"
			contact.save()

		return HttpResponse(status=200)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
def kickUser(request):
	if request.user is not None:
		groupName = request.data['groupName']
		userToKickUsername = request.data['username']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		if request.user.qwirkuser in qwirkGroup.admins.all():
			userToKick = QwirkUser.objects.get(user__username=userToKickUsername)
			userToKick.qwirkGroups.remove(qwirkGroup)

			text = json.dumps({
				"action": "removeGroup",
				"groupName": groupName
			})
			Group("user" + userToKickUsername).send({
				"text": text,
			})

			utils.sendMessageToAllUserGroup(qwirkGroup, request.user,
											userToKickUsername + " has been kicked by " + request.user.username, "informations")

			return HttpResponse(status=200)
		else:
			jsonResponse = JSONRenderer().render({'status': 'error', 'name': "NoAdminRight", 'message': 'You need to be admin for kick user'})
			return HttpResponse(jsonResponse, status=403)
	else:
		return HttpResponse(status=401)



@api_view(['POST'])
def banUser(request):
	if request.user is not None:
		groupName = request.data['groupName']
		userToBanUsername = request.data['username']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		if request.user.qwirkuser in qwirkGroup.admins.all():
			userToBan = QwirkUser.objects.get(user__username=userToBanUsername)
			qwirkGroup.blockedUsers.add(userToBan)
			userToBan.qwirkGroups.remove(qwirkGroup)

			text = json.dumps({
				"action": "removeGroup",
				"groupName": groupName
			})
			Group("user" + userToBanUsername).send({
				"text": text,
			})


			utils.sendMessageToAllUserGroup(qwirkGroup, request.user,
											userToBanUsername + " has been banned by " + request.user.username, "informations")

			return HttpResponse(status=200)
		else:
			jsonResponse = JSONRenderer().render({'status': 'error', 'name': "NoAdminRight", 'message': 'You need to be admin for banuser'})
			return HttpResponse(jsonResponse, status=403)
	else:
		return HttpResponse(status=401)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def userChannelAutocomplete(request):

	q = request.query_params.get('q', None)

	# Don't forget to filter out results depending on the visitor !
	if not request.user.is_authenticated():
		jsonResponse = JSONRenderer().render({"error": "authorization fail"})
		return HttpResponse(jsonResponse, status=401)

	users = User.objects.all()
	channels = QwirkGroup.objects.filter(isPrivate=False)


	result = dict()

	if q:
		usersStart = users.filter(username__istartswith=q)
		usersSearch = users.filter(username__icontains=q)


		channelsStart = channels.filter(name__istartswith=q)
		channelsSearch = channels.filter(name__icontains=q)

		# print(qsSearch)

		for user in usersStart:
			# print(result)
			if request.user != user:
				result[user.username] = { "name": user.username, "type": "user"}

		for user in usersSearch:
			# print(result)
			if request.user != user:
				result[user.username] = { "name": user.username, "type": "user"}

		for channel in channelsStart:
			# print(result)
			result[channel.name] = { "name": channel.name, "type": "channel"}

		for channel in channelsSearch:
			# print(result)
			result[channel.name] = { "name": channel.name, "type": "channel"}

	else:
		for user in users:
			if request.user != user:
				result[user.username] = { "name": user.username, "type": "user"}

		for channel in channels:
			result[channel.name] = { "name": channel.name, "type": "channel"}

	jsonResponse = JSONRenderer().render(result)
	print(jsonResponse)
	return HttpResponse(jsonResponse, status=200)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def userAutocomplete(request):

	q = request.query_params.get('q', None)

	# Don't forget to filter out results depending on the visitor !
	if not request.user.is_authenticated():
		jsonResponse = JSONRenderer().render({"error": "authorization fail"})
		return HttpResponse(jsonResponse, status=401)

	users = User.objects.all()

	result = dict()

	if q:
		usersStart = users.filter(username__istartswith=q)
		usersSearch = users.filter(username__icontains=q)

		# print(qsSearch)

		for user in usersStart:
			# print(result)
			if request.user != user:
				result[user.username] = { "name": user.username, "type": "user"}

		for user in usersSearch:
			# print(result)
			if request.user != user:
				result[user.username] = { "name": user.username, "type": "user"}

	else:
		for user in users:
			if request.user != user:
				result[user.username] = { "name": user.username, "type": "user"}

	jsonResponse = JSONRenderer().render(result)
	print(jsonResponse)
	return HttpResponse(jsonResponse, status=200)


@api_view(['POST'])
def changeAvatar(request):
	if request.user is not None:

		avatar = request.FILES['file']

		request.user.qwirkuser.avatar.delete(False)
		request.user.qwirkuser.avatar.save(request.user.username +'-avatar.jpg', avatar, save=True)

		jsonResponse = JSONRenderer().render({"name": request.user.qwirkuser.avatar.name})
		return HttpResponse(jsonResponse, status=200)
	else:
		return HttpResponse(status=401)


@api_view(['POST'])
def postFile(request):
	if request.user is not None:
		file = request.FILES['file']
		groupName = request.data['groupName']
		type = request.data['type']

		qwirkGroup = QwirkGroup.objects.get(name=groupName)

		#TODO security
		#if request.user.qwirkuser in qwirkGroup.qwirkuser_set.all() or request.user.qwirkuser in qwirkGroup.contact_set.all():

		message = Message(qwirkUser=request.user.qwirkuser, qwirkGroup=qwirkGroup, text=request.user.username + " upload a file", dateTime=datetime.now(), type=type)
		message.file.save(file.name, file)
		message.save()

		messageSerialized = MessageSerializer(message)

		text = json.dumps({
			"action": "new-message",
			"content": json.dumps(messageSerialized.data)
		})
		Group(groupName).send({
			"text": text,
		})

		if qwirkGroup.isContactGroup:
			for contact in qwirkGroup.contact_set.all():
				print(contact.qwirkUser)
				if contact.qwirkUser != request.user.qwirkuser:
					notification = Notification.objects.create(message=message, qwirkUser=contact.qwirkUser)
					notification.save()
					serializer = NotificationSerializerSimple(notification)
					text = json.dumps({
						"action": "notification",
						"notification": serializer.data
					})
					Group("user" + contact.qwirkUser.user.username).send({
						"text": text,
					})
		else:
			for qwirkUser in qwirkGroup.qwirkuser_set.all():
				print(qwirkUser)
				if qwirkUser != request.user.qwirkuser:
					notification = Notification.objects.create(message=message, qwirkUser=qwirkUser)
					notification.save()
					serializer = NotificationSerializerSimple(notification)
					text = json.dumps({
						"action": "notification",
						"notification": serializer.data
					})
					Group("user" + qwirkUser.user.username).send({
						"text": text,
					})
		return HttpResponse(status=200)
		#else:
		#	return HttpResponse(status=403)
	else:
		return HttpResponse(status=401)


def downloadFile(request):

	fileName = request.GET.get('fileName', "")
	pathToFile = path.join(settings.BASE_DIR, '../web-app/static/media/files/' + fileName)

	wrapper = FileWrapper(open(pathToFile, "rb"))
	content_type = mimetypes.guess_type(pathToFile)[0]

	print(content_type)

	response = HttpResponse(wrapper, content_type=content_type)
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fileName)
	#response['Content-Length']      = path.getsize(pathToFile)
	#response['X-Sendfile'] = smart_str(pathToFile)

	return response
