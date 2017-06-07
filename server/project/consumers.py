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
from rest_framework.renderers import JSONRenderer

from project import utils
from project.models import QwirkGroup, Contact, QwirkUser, Message, Notification
import json
import time
from project.chatbot import botActions

from project.serializer import MessageSerializer, QwirkUserSerializerSimple, NotificationSerializer, \
	NotificationSerializerSimple


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

			userIsInGroup = token.user.qwirkuser in QwirkGroup.objects.get(name=groupName).qwirkuser_set.all()
			print("userIsInGroup: " + str(userIsInGroup))

			userIsBanned = False

			if token.user.qwirkuser in QwirkGroup.objects.get(name=groupName).blockedUsers.all():
				print("user is banned")
				userIsBanned = True

			if contactRelationExist or (userIsInGroup and not userIsBanned):
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
				qwirkGroup = QwirkGroup.objects.get(name=kwargs["groupname"])  # TODO check with exist or with try catch but not sur because check in connect need to be tested

				if content["action"] == "message":

					utils.sendMessageToGroup(qwirkGroup, user, content["content"]["text"], "message")

					self.chatbot(qwirkGroup, user, text=content["content"]["text"])

				elif content["action"] == "call":
					Group(kwargs["groupname"]).send({
						"text": json.dumps(content),
					})
				elif content["action"] == "get-message":

					try:
						Notification.objects.filter(message__qwirkGroup__name=kwargs["groupname"],
																	qwirkUser=user.qwirkuser).delete()
					except Notification.DoesNotExist:
						pass

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

					groupInfo = dict()

					groupInfo["isPrivate"] = qwirkGroup.isPrivate
					groupInfo["isContactGroup"] = qwirkGroup.isContactGroup

					if user.qwirkuser in qwirkGroup.admins.all():
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
								for qwirkUser in groupInfo["qwirkUsers"]:
									qwirkUser["isAdmin"] = True
								groupInfo["statusContact"] = contact.status
					else:
						qwirkUsers = qwirkGroup.qwirkuser_set.all()
						for qwirkUser in qwirkUsers:
							groupInfo["qwirkUsers"].append(QwirkUserSerializerSimple(qwirkUser).data)
							for qwirkUser in groupInfo["qwirkUsers"]:
								qwirkUser["isAdmin"] = qwirkUser in qwirkGroup.admins.all()
						groupInfo["titleGroupName"] = qwirkGroup.name
					text = {
						"action": "group-informations",
						"content": json.dumps(groupInfo)
					}
					self.send(text)
				elif content["action"] == "accept-contact-request":
					if qwirkGroup.isContactGroup:
						contacts = qwirkGroup.contact_set.all()
						for contact in contacts:
							contact.status = "Friend"
							contact.save()

						requestMessage = qwirkGroup.message_set.get(type='requestMessage')
						requestMessage.type = "acceptMessage"
						requestMessage.save()

						utils.sendFriendshipResponse(qwirkGroup, user, "acceptMessage", requestMessage)


				elif content["action"] == "decline-contact-request":
					if qwirkGroup.isContactGroup:
						contacts = qwirkGroup.contact_set.all()
						for contact in contacts:
							contact.status = "Refuse"
							contact.save()

						requestMessage = qwirkGroup.message_set.get(type='requestMessage')
						requestMessage.type = "refuseMessage"
						requestMessage.save()


						utils.sendFriendshipResponse(qwirkGroup, user, "refuseMessage", requestMessage)
				elif content["action"] == "remove-contact":
					qwirkGroup.delete()
				elif content["action"] == "block-contact":
					if qwirkGroup.isContactGroup:
						for contact in qwirkGroup.contact_set.all():
							contact.status = "Block"
							contact.save()

						requestMessage = qwirkGroup.message_set.get(type='requestMessage')
						requestMessage.type = "blockMessage"
						requestMessage.save()

						utils.sendFriendshipResponse(qwirkGroup, user, "blockMessage", requestMessage)
					else:
						username = content["content"]["username"]
						userToBlock = QwirkUser.objects.get(user__username=username)
						qwirkGroup.blockedUsers.add(userToBlock)

						textMessage = user.username + " has blocked " + userToBlock.user.username

						utils.sendMessageToGroup(qwirkGroup, user, textMessage, "informations")

		else:
			print("no groupname in url")

	def chatbot(self, qwirkGroup, user, text):
		text = text.replace('<br />', ' ')
		occurenceBot = text.count('@bot')
		print("occurenceBot = " + str(occurenceBot))
		if occurenceBot > 0:

			print("calling bot " + str(occurenceBot) + " times")
			textSplit = text.split('@bot')
			"""beginWithBot = text.startswith('@bot')
			if beginWithBot:
				indexSplit = 0
			else:
				indexSplit = 1"""

			indexSplit = 1

			print("textSplit = " + str(textSplit))
			for i in range(0,occurenceBot):

				actionSplit = textSplit[indexSplit].split()

				for action in botActions:
					print("actionSplit[0] = " + actionSplit[0])
					print("action['action'] = " + action["action"])
					if actionSplit[0] == action["action"]:
						parameters = list()
						for j in range(0, action["parameters"]):
							parameters.append(actionSplit[j])
						action["function"](qwirkGroup, user)
				indexSplit += 1




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
