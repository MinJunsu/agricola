from rest_framework import serializers
from .models import Room, GameResult, GameResultDetail
from accounts.serializers import UserSerializer

class RoomSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'creator', 'mode', 'users']

        @staticmethod
        def get_user(queryset):
            return queryset.users.all()

class GameResultDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GameResultDetail
        fields = ['user', 'score']

class GameResultSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    game_result_detail = GameResultDetailSerializer(many=True, read_only=True)

    class Meta:
        model = GameResult
        fields = ['room', 'winner', 'createdAt', 'finished', 'game_result_detail']
