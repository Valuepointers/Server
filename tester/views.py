import requests

from django.conf import settings
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class KakaoSignUpView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        authorization_code = request.data.get("code")
        # print(authorization_code)

        #################### get access token ####################
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
        response_json = response.json()
        access_token = response_json.get("access_token")
        # print(access_token)
        if access_token == None:
            return Response(response.content, status=response.status_code)
        #################### end ####################

        #################### get User Data ####################        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        ###### User Data Request ######
        kakao_profile = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers=headers
        )
        profile_json = kakao_profile.json()
        # print(profile_json)
        ##### end #####
        
        ###### User Data Save ######
        kakao_id = profile_json["id"]
        email = profile_json["email"]
        # profile_image = profile_json['kakao_account']['profile']['thumbnail_image_url']
        user, created = User.objects.get_or_create(email=email, kakao_id=kakao_id)
        # user.profile_image = profile_image
        user.save()
        ##### end #####
        #################### end ####################        

        #################### create JWT Token ####################
        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)
        #################### end ####################

        return Response(
            {"created": created, "access": access_token, "refresh": refresh_token}
        )
