from django.contrib.auth.models import User, Group
from django.db import models


class QwirkGroup(models.Model):
	name = models.CharField(max_length=20, unique=True)
	isPrivate = models.BooleanField()
	isContactGroup = models.BooleanField()
	admins = models.ManyToManyField('QwirkUser', related_name='admins')
	blockedUsers = models.ManyToManyField('QwirkUser', related_name='blockedUsers', blank=True)

	def __str__(self):
		return str(self.name)


# Create your models here.
class QwirkUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	birthDate = models.DateField(null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	contacts = models.ManyToManyField('Contact', blank=True)
	qwirkGroups = models.ManyToManyField(QwirkGroup, blank=True)
	status = models.CharField(max_length=10)

	def __str__(self):
		return str(self.user.username)


class Contact(models.Model):
	qwirkUser = models.ForeignKey(QwirkUser, on_delete=models.CASCADE)
	qwirkGroup = models.ForeignKey(QwirkGroup, on_delete=models.CASCADE)

	status = models.CharField(max_length=10)

	def __str__(self):
		return str(self.qwirkUser.user.username)


class Message(models.Model):
	qwirkUser = models.ForeignKey(QwirkUser, on_delete=models.CASCADE)
	qwirkGroup = models.ForeignKey(QwirkGroup, on_delete=models.CASCADE)
	text = models.TextField()
	dateTime = models.DateTimeField(auto_now=True)
	type = models.TextField()


class Notification(models.Model):
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	qwirkUser = models.ForeignKey(QwirkUser, related_name="notifications", on_delete=models.CASCADE)
	dateRead = models.DateTimeField(null=True, blank=True)
