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
        fields = ('id', 'name', 'private')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contact
        fields = ('user', 'status')


class QwirkUserSerializer(serializers.ModelSerializer):
    qwirkGroups = QwirkGroupSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = QwirkUser
        fields = ('id', 'user', 'bio', 'birthDate', 'qwirkGroups', 'contacts')
        depth = 1
