from django.contrib import admin

from cards.models import CardEffect


# Register your models here.

@admin.register(CardEffect)
class CardEffectAdmin(admin.ModelAdmin):
    pass
