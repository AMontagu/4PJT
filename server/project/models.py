from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class QwirkUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthDate = models.DateField(null=True)
    bio = models.TextField(null=True)
