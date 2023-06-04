from django.apps import AppConfig

from core.redis import connection


class CardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cards"

    def ready(self):
        super().ready()
        from .models import Card
        redis = connection()
        cards = Card.objects.all().values('card_number', 'command', 'name', 'score')
        redis.hset('commands', mapping={card['card_number']: card['command'] for card in cards})
        redis.hset('cards', mapping={card['card_number']: str({
            'card_number': card['card_number'],
            'name': card['name'],
            'score': card['score']
        }) for card in cards})
