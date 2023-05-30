from django.db import models


# Create your models here.
class Card(models.Model):
    card_number = models.CharField(max_length=16)
    card_type = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    cost = models.IntegerField()
    score = models.IntegerField()
    condition = models.CharField(max_length=100)
    command = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_use = models.BooleanField(default=False)
