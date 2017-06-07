import json

from channels import Group
from project.models import QwirkUser, QwirkGroup, Notification, Message
from project.serializer import MessageSerializer, NotificationSerializerSimple


def sendSomething(qwirkGroup, user, *args):
	if len(args) > 0:
		message = Message.objects.create(qwirkUser=user.qwirkuser, qwirkGroup=qwirkGroup, text=str(args[0]),
										 type="botResponse")
		message.save()

		messageSerialized = MessageSerializer(message)

		text = json.dumps({
			"action": "new-message",
			"content": json.dumps(messageSerialized.data)
		})
		Group(qwirkGroup.name).send({
			"text": text,
		})

		if qwirkGroup.isContactGroup:
			for contact in qwirkGroup.contact_set.all():
				print(contact.qwirkUser)
				if contact.qwirkUser != user.qwirkuser:
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
				if qwirkUser != user.qwirkuser:
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


def sayHello(qwirkGroup, user, *args):
	sendSomething(qwirkGroup, user, "Hello !")


def kickUser(qwirkGroup, user, *args):
	if len(args) > 0:
		if user.qwirkuser in qwirkGroup.admins:
			try:
				qwirkUserToKick = QwirkUser.objects.get(user__username=args[0])
				qwirkUserToKick.qwirkGroups.remove(qwirkGroup)
				sendSomething(qwirkGroup, user, "User " + str(args[0]) + " has been kicked")
			except QwirkUser.DoesNotExist:
				sendSomething(qwirkGroup, user, "User not in group")


def banUser(qwirkGroup, user, *args):
	if len(args) > 0:
		if user.qwirkuser in qwirkGroup.admins:
			try:
				qwirkUserToBan = QwirkUser.objects.get(user__username=args[0])
				qwirkUserToBan.qwirkGroups.remove(qwirkGroup)
				qwirkGroup.blockedUsers.add(qwirkUserToBan)
				sendSomething(qwirkGroup, user, "User " + str(args[0]) + " has been kicked")
			except QwirkUser.DoesNotExist:
				sendSomething(qwirkGroup, user, "User not in group")












botActions = [{"action": 'hello', "parameters": 0, "function": sayHello},
			  {"action": 'kick', "parameters": 1, "function":kickUser}, {"action": 'ban', "parameters": 1, "function":banUser}]