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

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, kakao_id=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, kakao_id=kakao_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, kakao_id=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, kakao_id, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    kakao_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['kakao_id']  # email은 USERNAME_FIELD로 사용되므로 REQUIRED_FIELDS에 포함시키지 않음

