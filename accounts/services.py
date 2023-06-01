import os
from typing import Optional

import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from accounts.models import User, Profile


def kakao_get_user_info(access_token):
    url = 'https://kapi.kakao.com/v2/user/me'
    response = requests.get(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {access_token}'
    })

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Kakao.')

    user_info = response.json()

    return user_info


def kakao_get_access_token(url, code):
    redirect_url = settings.BASE_BACKEND_URL + '/auth/kakao/callback/'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_REST_API_KEY,
        'redirect_uri': redirect_url,
        'code': code
    }

    response = requests.post(url, data=data)

    if not response.ok:
        raise ValidationError('kakao_code is invalid')

    access_token = response.json().get('access_token')

    return access_token


def user_create(email: str, nickname: Optional[str], avatar: Optional[str]):
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            'email': email,
        }
    )

    Profile.create(
        user=user, nickname=nickname, avatar=avatar,
    )

    return user
