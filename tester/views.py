import requests

from django.conf import settings
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from .models import User
from .models import User


BASE_URL = settings.BASE_URL
KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
REDIRECT_URI = settings.REDIRECT_URI
CLIENT_SECRET_KEY = settings.CLIENT_SECRET_KEY


# authorization code
def kakao_auth_code(request):
    redirect_uri = BASE_URL + REDIRECT_URI
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={redirect_uri}&response_type=code"
    )


def get_user_data(access_token):
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        ###### User Data Request ######
        kakao_profile = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers=headers
        )
        profile_json = kakao_profile.json()
        print(profile_json)
        ##### end #####

        ##### User Data Get #####
        kakao_id = profile_json.get("id")
        if not kakao_id:
            print("no kakao id")
            return None, None, None

        username = profile_json.get("properties", {}).get("nickname")
        if not username:
            print("no nickname")
            username=kakao_id

        email = profile_json.get("email")  # .get 메소드를 사용하여 KeyError를 방지
        if not email:
            print("no email")
            email = f"user_{kakao_id}@example.com"
        ##### end #####
        return username, kakao_id, email
    except Exception as e:
        print(e)
        return None, None, None

def get_access_token(authorization_code):
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_REST_API_KEY,
            "redirect_uri": BASE_URL + REDIRECT_URI,
            "code": authorization_code,
            "client_secret": CLIENT_SECRET_KEY,
        }
        response = requests.post(
            "https://kauth.kakao.com/oauth/token", headers=headers, data=data
        )
        # print(response)
        return response
    except Exception as e:
        print(e)
        return None

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter  # 카카오 OAuth2 어댑터 사용

    def post(self, request, *args, **kwargs):
        # 카카오로부터 authorization code 받기
        authorization_code = request.data.get("code")
        print(authorization_code)
        #################### get token ####################
        response = get_access_token(authorization_code)
        response_json = response.json()
        access_token = response_json.get("access_token")
        if not access_token:
            return Response(response.content, status=response.status_code)
        #################### end ####################

        #################### get User Data ####################        
        username, kakao_id, email = get_user_data(access_token)
        if not kakao_id:
            return Response({"error": "Failed to retrieve user data from Kakao"}, status=status.HTTP_400_BAD_REQUEST)
        #################### end ####################


        #################### User Check ####################
        try:
            ##### login #####
            user = User.objects.get(kakao_id=kakao_id)
            # 사용자가 존재하는 경우, JWT 토큰 생성 및 반환
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "username": user.username,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "detail": "Existing user"
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            ##### sign up #####
            user = User.objects.create_user(username=username, email=email, kakao_id=kakao_id)
            user.set_unusable_password()  # 비밀번호는 카카오 로그인으로 관리되므로 설정하지 않음
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "username": user.username,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "created": True  # 사용자가 새로 생성되었음을 나타냄
            })