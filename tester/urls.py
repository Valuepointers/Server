from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import KakaoLogin, kakao_auth_code

urlpatterns = [
    path('kakao/code/', kakao_auth_code),
    path('kakao/login/', KakaoLogin.as_view()),
    path('kakao/login/refresh/', TokenRefreshView.as_view()),
    
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls'))
]
