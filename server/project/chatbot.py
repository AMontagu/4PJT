import json

from channels import Group

from project import utils
from project.models import QwirkUser, QwirkGroup, Notification, Message
from project.serializer import MessageSerializer, NotificationSerializerSimple


def sendSomething(qwirkGroup, user, *args):
	if len(args) > 0:
		utils.sendMessageToAllUserGroup(qwirkGroup, user, args[0], "botResponse")


def sayHello(qwirkGroup, user, *args):
	sendSomething(qwirkGroup, user, "Hello !")


def kickUser(qwirkGroup, user, parameters):
	if len(parameters) > 0:
		print(parameters[0])
		if user.qwirkuser in qwirkGroup.admins.all():
			try:
				qwirkUserToKick = QwirkUser.objects.get(user__username=parameters[0])
				qwirkUserToKick.qwirkGroups.remove(qwirkGroup)
				sendSomething(qwirkGroup, user, "User " + str(parameters[0]) + " has been kicked")


				utils.sendMessageToAllUserGroup(qwirkGroup, user,
												parameters[0] + " has been kicked by " + user.username, "informations")

				textUserLeave = json.dumps({
					"action": "userLeave",
					"username": user.username
				})
				utils.sendToQwirkGroup(qwirkGroup, user, textUserLeave)

			except QwirkUser.DoesNotExist:
				sendSomething(qwirkGroup, user, "User not in group")
		else:
			sendSomething(qwirkGroup, user, "You are not an admin you can't do that !")


def banUser(qwirkGroup, user, parameters):
	if len(parameters) > 0:
		if user.qwirkuser in qwirkGroup.admins.all():
			try:
				qwirkUserToBan = QwirkUser.objects.get(user__username=parameters[0])
				qwirkUserToBan.qwirkGroups.remove(qwirkGroup)
				qwirkGroup.blockedUsers.add(qwirkUserToBan)
				sendSomething(qwirkGroup, user, "User " + str(parameters[0]) + " has been kicked")

				utils.sendMessageToAllUserGroup(qwirkGroup, user,
												parameters[0] + " has been banned by " + user.username, "informations")

				textUserLeave = json.dumps({
					"action": "userLeave",
					"username": user.username
				})
				utils.sendToQwirkGroup(qwirkGroup, user, textUserLeave)

			except QwirkUser.DoesNotExist:
				sendSomething(qwirkGroup, user, "User not in group")
		else:
			sendSomething(qwirkGroup, user, "You are not an admin you can't do that !")












botActions = [{"action": 'hello', "parameters": 0, "function": sayHello},
			  {"action": 'kick', "parameters": 1, "function":kickUser}, {"action": 'ban', "parameters": 1, "function":banUser}]