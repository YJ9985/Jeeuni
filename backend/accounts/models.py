from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        extra_fields.setdefault('birth_date', '2000-01-01')
        extra_fields.setdefault('first_name', 'Ad')
        extra_fields.setdefault('last_name', 'Min')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    kakao_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    
    # 생년월일
    birth_date = models.DateField()

    # 소셜 로그인 제공자 정보 (google, kakao)
    provider = models.CharField(max_length=30, blank=True)

    objects = CustomUserManager()  

    @property
    def name(self):
        return f"{self.first_name}{self.last_name}"
