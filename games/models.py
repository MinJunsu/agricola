from django.db import models

from accounts.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    @staticmethod
    def create_room(name, creator, mode, password=None):
        room = Room.objects.create(name=name, creator=creator, mode=mode, password=password)
        return room

    @staticmethod
    def get_room_list():
        room_list = Room.objects.all()
        return room_list


class GameResult(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_game_result(room, winner):
        game_result = GameResult.objects.create(room=room, winner=winner)
        return game_result


class GameResultDetail(models.Model):
    game = models.ForeignKey(GameResult, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    @staticmethod
    def create_game_result_detail(game, user, score):
        game_result_detail = GameResultDetail.objects.create(game=game, user=user, score=score)
        return game_result_detail

    @staticmethod
    def get_game_result_detail(game):
        game_result_detail = GameResultDetail.objects.filter(game=game)
        return game_result_detail
