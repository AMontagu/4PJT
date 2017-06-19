"""
File that defined all the serializer used in our API

See http://www.django-rest-framework.org/api-guide/serializers/
See http://www.django-rest-framework.org/api-guide/fields/
See http://www.django-rest-framework.org/api-guide/relations/
"""
from rest_framework import serializers
from project.models import *
from django.contrib.auth.models import User, Group

class QwirkGroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = QwirkGroup
		fields = ('id', 'name', 'isPrivate', 'isContactGroup')


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'first_name', 'last_name')
		extra_kwargs = {
			'password': {'write_only': True}
		}


class QwirkUserSerializerSimple(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)

	class Meta:
		model = QwirkUser
		fields = ('user', 'bio', 'birthDate', 'status', 'avatar')
		depth = 1


class MessageSerializer(serializers.ModelSerializer):
	qwirkGroup = QwirkGroupSerializer(read_only=True)
	qwirkUser = QwirkUserSerializerSimple(read_only=True)

	class Meta:
		model = Message
		fields = ('qwirkUser', 'qwirkGroup', 'text', 'dateTime', 'type', 'file')


class MessageSerializerSimple(serializers.ModelSerializer):
	qwirkGroup = serializers.SlugRelatedField(
		read_only=True,
		slug_field='name'
	)

	qwirkUser = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Message
		fields = ('qwirkGroup', 'qwirkUser', 'text', 'dateTime', 'type', 'file')


class NotificationSerializer(serializers.ModelSerializer):
	qwirkUser = QwirkUserSerializerSimple(read_only=True)
	message = MessageSerializer(read_only=True)

	class Meta:
		model = Notification
		fields = ('message', 'qwirkUser', 'dateRead')


class NotificationSerializerSimple(serializers.ModelSerializer):
	message = MessageSerializerSimple(read_only=True)

	class Meta:
		model = Notification
		fields = ('message', 'dateRead')


class ContactSerializer(serializers.ModelSerializer):
	qwirkUser = QwirkUserSerializerSimple(read_only=True)
	qwirkGroup = QwirkGroupSerializer(read_only=True)

	class Meta:
		model = Contact
		fields = ('qwirkUser', 'status', 'qwirkGroup')


class QwirkUserSerializer(serializers.ModelSerializer):
	qwirkGroups = QwirkGroupSerializer(many=True, read_only=True)
	contacts = ContactSerializer(many=True, read_only=True)
	user = UserSerializer(read_only=True)
	notifications = NotificationSerializerSimple(many=True, read_only=True)

	class Meta:
		model = QwirkUser
		fields = ('notifications', 'user', 'bio', 'birthDate', 'qwirkGroups', 'contacts', 'status', 'avatar')