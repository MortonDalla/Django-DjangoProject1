
from django.db import models

from django.db import models
from django.urls import reverse

class RegisterUsers(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    user_name = models.CharField(max_length=120)
    password = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=200)
    description = models.TextField(blank=True)
    contact_numbers = models.CharField(max_length=130)

class Clients(models.Model):
    client_name = models.CharField(max_length=300)
    contact_person = models.CharField(max_length=300)
    contact_number = models.IntegerField()