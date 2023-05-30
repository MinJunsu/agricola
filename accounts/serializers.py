from rest_framework import serializers

from accounts.models import Profile, UserConfig, Friend


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'social_link', 'image', 'address', 'point', 'point_history', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'
