from django.contrib import admin

from cards.models import CardEffect, Card


# Register your models here.

@admin.register(CardEffect)
class CardEffectAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'effect', 'command']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'command']
    ordering = ['card_number']
