from django.db import models
from .tour import Tour

class Comment(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=500)