"""
In this file we found all our websocket consumers.

See https://channels.readthedocs.io/en/latest/

See https://github.com/EvotionTeam/hease-robot/wiki/WebSocket-communication
"""
import base64
import os

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.generic.websockets import WebsocketConsumer, JsonWebsocketConsumer, BaseConsumer
from channels import Group
import json
from server.customLogging import *


class TestJsonConsumer(JsonWebsocketConsumer):
	"""
	Test websocket for testing purpose.

	See https://channels.readthedocs.io/en/latest/generics.html
	"""
	http_user = True

	# Set to True if you want them, else leave out
	strict_ordering = False
	slight_ordering = False

	def connection_groups(self, **kwargs):
		print("connection test groups json")
		return ["test"]

	def connect(self, message, **kwargs):
		print("connect test json")
		text = json.dumps({
			"action": "add",
		})
		Group("test").send({
			"text": text,
		})

	def receive(self, content, **kwargs):
		print("receive test json :")
		print(content)
		# self.send(content)
		text = json.dumps({
			"action": "message",
			"user": self.message.user.username,
			"authenticated": self.message.user.is_authenticated(),
			"message": content["text"],
		})
		Group("test").send({
			"text": text,
		})

	def disconnect(self, message, **kwargs):
		print("disconnect test json")
		text = json.dumps({
			"action": "disconnect",
		})
		Group("test").send({
			"text": text,
		})


class ChatConsumer(JsonWebsocketConsumer):
	"""
	Handle web socket exchange in our app

	See https://channels.readthedocs.io/en/latest/generics.html
	"""
	http_user = True
	# Set to True if you want them, else leave out
	strict_ordering = False
	slight_ordering = False

	def connection_groups(self, **kwargs):
		listGroupName = list()
		for group in self.message.user.groups:
			listGroupName.append(group.name)
		return listGroupName

	def connect(self, message, **kwargs):
		LOGDEBUG("connection ApiJsonConsumer")

		if self.message.user.is_authenticated():
			text = {
				"action": "connected",
			}
			self.send(text)
		else:
			text = {
				"action": "not-logged-in",
			}
			self.send(text)
			self.close()

	def receive(self, content, **kwargs):
		LOGINFO("receive ApiJsonConsumer json :")
		LOGINFO(content)

	def disconnect(self, message, **kwargs):
		LOGINFO("disconnect ApiJsonConsumer json")


def ws_add(message):
	LOGWARN("add not in project protocole :")
	LOGWARN(message.content)
	LOGWARN(message.reply_channel)


# Connected to websocket.disconnect
def ws_disconnect(message):
	LOGWARN("disconnect not in project protocole :")
	LOGWARN(message.content)


def ws_message(message):
	LOGWARN("message not in project protocole :")
	LOGWARN(message.content)
	LOGWARN(message.content['text'])
