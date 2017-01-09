"""
In this file we found all our websocket consumers.

See https://channels.readthedocs.io/en/latest/

See https://github.com/EvotionTeam/hease-robot/wiki/WebSocket-communication
"""
import base64
import datetime

from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.generic.websockets import WebsocketConsumer, JsonWebsocketConsumer, BaseConsumer
from django.utils.timezone import utc
from rest_framework.authtoken.models import Token
from channels import Group
import json


def checkToken(url):
	if "token" in url:
		try:
			token = Token.objects.select_related('user').get(key=url["token"])
		except Token.DoesNotExist:
			print("invalid token in url")
			return False

		if not token.user.is_active:
			print("invalid token User inactive or deleted.")
			return False

		utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

		if token.created < utc_now - datetime.timedelta(hours=24):
			print("Token has expired")
			return False
		print("user " + token.user.username)
		return True
	else:
		print("No token in url")
		return False

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
		if "groupname" in kwargs:
			print("connection to group" + kwargs["groupname"])
			return [kwargs["groupname"]]
		else:
			print("no groupname in url")

	def connect(self, message, **kwargs):
		print("connect Chat json")
		if not checkToken(kwargs):
			print("not-authorized connection")
			text = {
				"action": "not-authorized-connection",
			}
			self.send(text)
			self.close()


	def receive(self, content, **kwargs):
		print("receive Chat json :")
		print(content)

		if "groupname" in kwargs:
			text = json.dumps({
				"action": "message",
				"message": content["text"],
			})
			"""Group(kwargs["groupname"]).send({
				"text": text,
			})"""
			Group(kwargs["groupname"]).send({
				"text": text,
			})
		else:
			print("no groupname in url")

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
