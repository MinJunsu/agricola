from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User, Profile
from .services import (
    kakao_get_user_info, user_create,
)


class KakaoLoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        access_token = self.request.data['access_token']
        info = kakao_get_user_info(access_token=access_token)
        account = info['kakao_account']
        user: User = user_create(email=account['email'], nickname=account['profile']['nickname'],
                                 avatar=account['profile'].get('profile_image_url', None))
        token = TokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        })
