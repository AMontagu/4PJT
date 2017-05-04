"""
In this file we found all our websocket consumers.

See https://channels.readthedocs.io/en/latest/

See https://github.com/EvotionTeam/hease-robot/wiki/WebSocket-communication
"""
import base64
import datetime

from django.core import serializers
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.generic.websockets import WebsocketConsumer, JsonWebsocketConsumer, BaseConsumer
from django.utils.timezone import utc
from rest_framework.authtoken.models import Token
from channels import Group
from project.models import QwirkGroup, Contact, QwirkUser, Message, Notification
import json
import time

from project.serializer import MessageSerializer, QwirkUserSerializerSimple


def checkToken(url, isUser):
	if "token" in url:
		try:
			token = Token.objects.select_related('user').get(key=url["token"])
		except Token.DoesNotExist:
			print("invalid token in url")
			return False, None

		if not token.user.is_active:
			print("invalid token User inactive or deleted.")
			return False, None

		utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

		if token.created < utc_now - datetime.timedelta(hours=24):
			print("Token has expired")
			return False, None
		print("user " + token.user.username)

		if isUser:
			return checkUser(url, token)
		else:
			return checkGroup(url, token)

	else:
		print("No token in url")
		return False, None


def checkGroup(url, token):
	if "groupname" in url:
		groupName = url["groupname"]
		print("connection to group " + groupName)
		if QwirkGroup.objects.filter(name=groupName).exists():
			contactRelationExist = Contact.objects.filter(qwirkGroup__name=groupName,
			                                              qwirkUser=token.user.qwirkuser).exists()  # Check if the current user logged in with token is a contact of the group he try to connect
			print("contactRelationExist: " + str(contactRelationExist))
			userIsInGroup = QwirkUser.objects.filter(qwirkGroups__name=groupName).exists()
			print("userIsInGroup: " + str(userIsInGroup))
			if contactRelationExist or userIsInGroup:
				return True, token.user

	return False, None


def checkUser(url, token):
	if "username" in url:
		username = url["username"]
		print("user connected: " + username + " token belong to: " + token.user.username)
		if token.user.username == username:
			return True, token.user

	return False, None


class ChatJsonConsumer(JsonWebsocketConsumer):
	"""
	Handle the groups of all the robots for broadcasting informations to all the robots

	see https://channels.readthedocs.io/en/latest/generics.html
	"""
	http_user = True
	# Set to True if you want them, else leave out
	strict_ordering = False
	slight_ordering = False

	def connection_groups(self, **kwargs):
		print("connection Chat groups json")
		return [kwargs["groupname"]]

	def connect(self, message, **kwargs):
		print("connect Chat json")
		goodTokenAndUserInGroup, user = checkToken(kwargs, False)
		if goodTokenAndUserInGroup:
			self.message.reply_channel.send({"accept": True})
		else:
			print("not-authorized connection")
			self.message.reply_channel.send({"close": True})

	def receive(self, content, **kwargs):
		print("receive Chat json :")
		print(content)

		if "groupname" in kwargs:

			goodTokenAndUserInGroup, user = checkToken(kwargs, False)

			if goodTokenAndUserInGroup:

				if content["action"] == "message":
					qwirkGroup = QwirkGroup.objects.get(name=kwargs["groupname"])# TODO check with exist or with try catch but not sur because check in connect need to be tested

					message = Message.objects.create(qwirkUser=user.qwirkuser, qwirkGroup=qwirkGroup, text=content["content"]["text"])
					message.save()

					messageSerialized = MessageSerializer(message)

					text = json.dumps({
						"action": "new-message",
						"content": json.dumps(messageSerialized.data)
					})
					Group(kwargs["groupname"]).send({
						"text": text,
					})

					# NOTIFICATION PART

					notification = json.dumps({
						"action": "new-message",
						"groupname": qwirkGroup.name
					})

					if qwirkGroup.isContactGroup:
						for contact in qwirkGroup.contact_set.all():
							print(contact.qwirkUser)
							notification = Notification.objects.create(message=message, qwirkUser=contact.qwirkUser)
							notification.save()
							Group("user" + contact.qwirkUser.user.username).send({
								"text": notification,
							})
					else:
						for qwirkUser in qwirkGroup.qwirkuser_set.all():
							print(qwirkUser)
							notification = Notification.objects.create(message=message, qwirkUser=qwirkUser)
							notification.save()
							Group("user" + qwirkUser.user.username).send({
								"text": notification,
							})

				elif content["action"] == "call":
					Group(kwargs["groupname"]).send({
						"text": json.dumps(content),
					})
				elif content["action"] == "get-message":
					messages = Message.objects.filter(qwirkGroup__name=kwargs["groupname"]).order_by("-dateTime")[int(content["content"]["startMessage"]):int(content["content"]["endMessage"])]
					messageToSend = list()
					for message in messages:
						messageToSend.append(MessageSerializer(message).data)
					# print(messageToSend)
					text = {
						"action": "saved-messages",
						"content": json.dumps(messageToSend)
					}
					self.send(text)
				elif content["action"] == "get-group-informations":
					groupName = kwargs["groupname"]

					print(groupName)

					qwirkGroup = QwirkGroup.objects.get(name=groupName)

					groupInfo = dict()

					groupInfo["isPrivate"] = qwirkGroup.isPrivate
					groupInfo["isContactGroup"] = qwirkGroup.isContactGroup

					if user.qwirkuser in qwirkGroup.admin.all():
						groupInfo["isAdmin"] = True
					else:
						groupInfo["isAdmin"] = False

					groupInfo["qwirkUsers"] = list()

					if groupInfo["isContactGroup"]:
						contacts = qwirkGroup.contact_set.all()
						for contact in contacts:
							if contact.qwirkUser.user.username != user.username:
								groupInfo["titleGroupName"] = contact.qwirkUser.user.username
								groupInfo["qwirkUsers"].append(QwirkUserSerializerSimple(contact.qwirkUser).data)
					else:
						qwirkUsers = qwirkGroup.qwirkuser_set.all()
						for qwirkUser in qwirkUsers:
							groupInfo["qwirkUsers"].append(QwirkUserSerializerSimple(qwirkUser).data)
						groupInfo["titleGroupName"] = qwirkGroup.name
					text = {
						"action": "group-informations",
						"content": json.dumps(groupInfo)
					}
					self.send(text)
		else:
			print("no groupname in url")

	def disconnect(self, message, **kwargs):
		print("disconnect Chat json")


class UserJsonConsumer(JsonWebsocketConsumer):
	"""
	Handle the groups of all the robots for broadcasting informations to all the robots

	see https://channels.readthedocs.io/en/latest/generics.html
	"""
	http_user = True
	# Set to True if you want them, else leave out
	strict_ordering = False
	slight_ordering = False

	def connection_groups(self, **kwargs):
		print("connection Chat groups json")
		return ["user" + kwargs["username"]]

	def connect(self, message, **kwargs):
		print("connect Chat json")
		goodTokenAndUser, user = checkToken(kwargs, True)
		if goodTokenAndUser:
			self.message.reply_channel.send({"accept": True})
		else:
			print("not-authorized connection")
			self.message.reply_channel.send({"close": True})

	def receive(self, content, **kwargs):
		print("receive user json :")
		print(content)
		print("strange this consumer is only for notification to user")

	def disconnect(self, message, **kwargs):
		print("disconnect Chat json")


def ws_add(message):
	print("add not in hease protocole :")
	print(message.content)
	print(message.reply_channel)


# Connected to websocket.disconnect
def ws_disconnect(message):
	print("disconnect not in hease protocole :")
	print(message.content)


def ws_message(message):
	print("message not in hease protocole :")
	print(message.content)
	print(message.content['text'])
