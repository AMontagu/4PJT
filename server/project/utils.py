import json

from channels import Group

from project.models import Message, Notification
from project.serializer import MessageSerializer, NotificationSerializerSimple, ContactSerializer


def sendToQwirkGroup(qwirkGroup, currentUser, element):
	if currentUser.qwirkuser in qwirkGroup.qwirkuser_set.all() and currentUser.qwirkuser not in qwirkGroup.blockedUsers.all():
		Group(qwirkGroup.name).send({
			"text": element,
		})
	else:
		print("user not in group or banned")

def sendCommandToAllUserGroup(qwirkGroup, currentUser, text):
	if qwirkGroup.isContactGroup:
		for contact in qwirkGroup.contact_set.all():
			if contact.qwirkUser != currentUser.qwirkuser:
				Group("user" + contact.qwirkUser.user.username).send({
					"text": text,
				})
	else:
		for qwirkUser in qwirkGroup.qwirkuser_set.all():
			if qwirkUser != currentUser.qwirkuser:
				Group("user" + qwirkUser.user.username).send({
					"text": text,
				})


def sendFriendshipResponse(qwirkGroup, currentUser, friendShipResponse, message):
	text = json.dumps({
		"action": "friendShipResponse",
		"friendShipResponse": friendShipResponse
	})
	Group(qwirkGroup.name).send({
		"text": text,
	})

	for contact in qwirkGroup.contact_set.all():
		if contact.qwirkUser != currentUser.qwirkuser:
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

def sendMessageToAllUserGroup(qwirkGroup, currentUser, text, type):
	message = Message.objects.create(qwirkUser=currentUser.qwirkuser, qwirkGroup=qwirkGroup, text=str(text), type=type)
	message.save()

	messageSerialized = MessageSerializer(message)

	text = json.dumps({
		"action": "new-message",
		"content": json.dumps(messageSerialized.data)
	})
	sendToQwirkGroup(qwirkGroup, currentUser, text)


	# NOTIFICATION PART

	if qwirkGroup.isContactGroup:
		for contact in qwirkGroup.contact_set.all():
			if contact.qwirkUser != currentUser.qwirkuser:
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
			if qwirkUser != currentUser.qwirkuser:
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



def sendMessageToContact(contact, qwirkGroup, currentUser, text, type):
	message = Message.objects.create(qwirkUser=currentUser.qwirkuser, qwirkGroup=qwirkGroup,
									 text=str(text), type=type)
	message.save()

	notification = Notification.objects.create(message=message, qwirkUser=contact.qwirkuser)
	notification.save()

	notificationSerializer = NotificationSerializerSimple(notification)

	text = json.dumps({
		"action": "notification",
		"notification": notificationSerializer.data
	})
	Group("user" + contact.username).send({
		"text": text,
	})

