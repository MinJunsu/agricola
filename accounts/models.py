from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Profile(models.Model):
    nickname = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    plays = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @staticmethod
    def create(nickname, avatar):
        return Profile.objects.create(nickname=nickname, avatar=avatar)

    @staticmethod
    def follow(user, friend):
        if Friend.objects.filter(user=user, friend=friend).exists():
            raise RelationAlreadyExistException()
        Friend.objects.create(user=user, friend=friend)
        Friend.objects.create(user=friend, friend=user)

    @staticmethod
    def unfollow(user, friend):
        if not Friend.objects.filter(user=user, friend=friend).exists():
            raise RelationDoesNotExistException()
        Friend.objects.filter(user=user, friend=friend).delete()
        Friend.objects.filter(user=friend, friend=user).delete()


class UserConfig(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    isInvited = models.BooleanField(default=False)
    isMuted = models.BooleanField(default=False)


class Friend(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_friends')


class RelationAlreadyExistException(Exception):
    pass


class RelationDoesNotExistException(Exception):
    pass
