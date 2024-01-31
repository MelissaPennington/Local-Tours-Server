from django.db import models
from .user import User
from .state import State

class Tour(models.Model):
  
 name = models.CharField(max_length=50)
 description = models.CharField(max_length=250)
 price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
 address = models.CharField(max_length=100)
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 image = models.CharField(max_length=200)
 state = models.ForeignKey(State, on_delete=models.CASCADE)
