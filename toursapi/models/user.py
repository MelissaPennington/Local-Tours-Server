from django.db import models

class User(models.Model):
  username = models.CharField(max_length=55)
  uid = models.CharField(max_length=55)
  bio = models.CharField(max_length=250)
