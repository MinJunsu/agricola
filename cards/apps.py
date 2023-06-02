from django.apps import AppConfig

from core.redis import connection


class CardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cards"

    def ready(self):
        super().ready()
        from .models import Card
        redis = connection()
        cards = Card.objects.all().values('card_number', 'command')
        redis.hset('commands', mapping={card['card_number']: card['command'] for card in cards})
