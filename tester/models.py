from django.db import models

class Company(models.Model):
    country = models.CharField(max_length=100)
    founded = models.CharField(max_length=100)
    ipo_date = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    employees = models.CharField(max_length=100)
    ceo = models.CharField(max_length=100)
    ticker_symbol = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    fiscal_year = models.CharField(max_length=100)
    reporting_currency = models.CharField(max_length=100)
    cik_code = models.CharField(max_length=100)
    cusip_number = models.CharField(max_length=100)
    isin_number = models.CharField(max_length=100)
    employer_id = models.CharField(max_length=100)
    sic_code = models.CharField(max_length=100)

    def __str__(self):
        return self.ticker_symbol


import datetime
import requests
from requests.exceptions import RequestException, JSONDecodeError

from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random

def make_user_name_unique(old_user_name):
    new_user_name = f"{old_user_name}_{random.randint(1, 10000)}"
    while User.objects.filter(username=new_user_name).exists():
        new_user_name = f"{old_user_name}_{random.randint(1, 10000)}"
    return new_user_name

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, kakao_id=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if username:
                username = make_user_name_unique(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, kakao_id=kakao_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, kakao_id=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, kakao_id, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(max_length=255, unique=False, null=True, blank=True)  # username을 선택적 필드로 설정
    email = models.EmailField(unique=True)  # 이메일을 필수 필드로 설정
    kakao_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # 로그인 식별자를 이메일로 설정
    REQUIRED_FIELDS = ['username']  # username을 선택적 필드로 설정

    def __str__(self):
        return self.email
