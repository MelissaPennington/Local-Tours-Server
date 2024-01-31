from django.db import models
from .category import Category
from .tour import Tour

class TourCategory(models.Model):
  
 category = models.ForeignKey(Category, on_delete=models.CASCADE)
 tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
