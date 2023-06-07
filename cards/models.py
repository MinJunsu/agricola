from django.db import models


# Create your models here.
class Card(models.Model):
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    cost = models.CharField(max_length=400, null=True)
    condition = models.CharField(max_length=400, null=True)
    command = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.card_number.upper()


class CardEffect(models.Model):
    card_number = models.CharField(max_length=16)
    effect = models.CharField(max_length=20)
    command = models.CharField(max_length=300)
