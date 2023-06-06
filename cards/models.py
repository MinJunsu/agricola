from django.db import models


# Create your models here.
class Card(models.Model):
    card_number = models.CharField(max_length=16)
    card_type = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    command = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.card_number.upper()
