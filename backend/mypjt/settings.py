from pathlib import Path
import os
import sys
from dotenv import load_dotenv
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured
import hashlib

BASE_DIR = Path(__file__).resolve().parent.parent

# 실행 환경: local / prod
DJANGO_ENV = os.environ.get("DJANGO_ENV", "local")

# 로컬일 때만 .env.local 로드
if DJANGO_ENV != "prod":
    load_dotenv(BASE_DIR / ".env.local", override=True)

# DEBUG 플래그
DEBUG = DJANGO_ENV != "prod"

# SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY environment variable must be set.")

# ALLOWED_HOSTS 설정
raw_hosts = os.environ.get("ALLOWED_HOSTS", "")

hosts = [h.strip() for h in raw_hosts.split(",") if h.strip()]

if "*" in hosts:
    ALLOWED_HOSTS = ["*"]
else:
    # 비어있으면 로컬 호스트 설정
    ALLOWED_HOSTS = hosts or ["localhost", "127.0.0.1"]


CORS_ALLOWED_ORIGINS = [
    h.strip()
    for h in os.environ.get(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if h.strip()
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    h.strip()
    for h in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if h.strip()
]

# Database
if DJANGO_ENV == "prod":
    from urllib.parse import unquote
    
    # 환경변수 원본 값 가져오기 (strip 전)
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_USER = os.environ.get("DB_USER", "")
    DB_PASSWORD_RAW = os.environ.get("DB_PASSWORD", "")
    # URL 디코딩 시도 (인코딩되어 있으면 디코딩, 아니면 그대로)
    DB_PASSWORD = unquote(DB_PASSWORD_RAW) if DB_PASSWORD_RAW else ""
    DB_HOST = os.environ.get("DB_HOST", "")
    DB_PORT = os.environ.get("DB_PORT", "5432")

    # 필수 값 체크
    required_keys = {
        "DB_NAME": DB_NAME,
        "DB_USER": DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
        "DB_HOST": DB_HOST
    }

    
    for key, value in required_keys.items():
        if not value:
            raise ImproperlyConfigured(f"{key} is required in environment for production")
        if key == "DB_PASSWORD":
            # 비밀번호 해시만 출력 (보안)
            pw_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()
            # 특수문자 포함 여부 체크
            special_chars = set("!@#$%^&*()[]{}|\\:;\"'<>,.?/~`")
            has_special = any(c in special_chars for c in value)

    # 공백 제거 후 DB 설정
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME.strip(),
            "USER": DB_USER.strip(),
            "PASSWORD": DB_PASSWORD.strip(),
            "HOST": DB_HOST.strip(),
            "PORT": DB_PORT,
            "OPTIONS": {
                "sslmode": "require",
                "connect_timeout": 10,
            },
            # 연결 풀 설정 추가
            "CONN_MAX_AGE": 600,
        }
    }

else:
    # 로컬: SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Application definition
INSTALLED_APPS = [
    'accounts',
    'books',
    'literacy',
    # 서드파티 앱
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    # provider
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',
    # django 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'mypjt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mypjt.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth / Allauth
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Social login
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv("GOOGLE_CLIENT_ID"),
            'secret': os.getenv("GOOGLE_CLIENT_SECRET"),
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS':{
            'access_type': 'online',
        },
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    },
    'kakao': {
        'APP': {
            'client_id': os.getenv("KAKAO_CLIENT_ID"),
            'secret': os.getenv("KAKAO_CLIENT_SECRET"),
        },
        'SCOPE': [
            'profile_nickname',
        ]
    }
}

SOCIALACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSocialSignupForm'
}
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.MySocialAccountAdapter'
SOCIALACCOUNT_LOGIN_ON_GET = True

# DRF / JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer'
    )

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv("JWT_ACCESS_MIN", "30"))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "7"))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

REST_USE_JWT = True

# Security (HTTPS 배포 시 적용)
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}