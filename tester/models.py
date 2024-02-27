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
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, kakao_id, password=None, **extra_fields):
        if not kakao_id:
            raise ValueError('The given kakao_id must be set')

        user = self.model(
            kakao_id=kakao_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, kakao_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(kakao_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    kakao_id = models.CharField(max_length=255, unique=True)

    # profile_image = models.URLField(blank=True, null=True, default="")
    # company = models.CharField(max_length=255, blank=True, null=True)
    # following = models.ManyToManyField(
        # 'self', symmetrical=False, related_name='followers')
    # is_open = models.BooleanField(default=True)
    # is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'kakao_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.kakao_id

    def follow(self, kakao_id):
        user = User.objects.get(kakao_id=kakao_id)
        self.following.add(user)

    def unfollow(self, kakao_id):
        user = User.objects.get(kakao_id=kakao_id)
        self.following.remove(user)

    def is_following(self, kakao_id):
        return self.following.filter(kakao_id=kakao_id).exists()

    def is_followed_by(self, kakao_id):
        return self.followers.filter(kakao_id=kakao_id).exists()

    # def get_studies(self):
        # return list(self.joined_studies.all())
