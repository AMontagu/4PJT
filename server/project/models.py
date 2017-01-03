from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
class QwirkUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthDate = models.DateField(null=True)
    bio = models.TextField(null=True)
    contacts = models.ManyToManyField('self', null=True)
    groups = models.ManyToManyField(Group, null=True)

    def __str__(self):
        return str(self.user.username)
