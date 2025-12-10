from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# DJANGO_ENV: local / prod (기본값은 local)
DJANGO_ENV = os.getenv("DJANGO_ENV", "local")

# 1) env 파일 경로 결정
if DJANGO_ENV == "prod":
    env_path = BASE_DIR / ".env.prod"
else:
    env_path = BASE_DIR / ".env.local"

# 2) env 파일 로드 (파일이 없어도 python-dotenv는 조용히 넘어감)
load_dotenv(env_path, override=False)

# 3) 공통 환경변수 읽기
SECRET_KEY = os.getenv("SECRET_KEY")
if DJANGO_ENV == "prod" and not SECRET_KEY:
    # prod에서는 무조건 SECRET_KEY가 있어야 하니까 방어 로직
    raise ImproperlyConfigured("SECRET_KEY must be set in environment for prod")

DEBUG = DJANGO_ENV != "prod"   # prod이면 False, 나머지는 True

# CORS/CSRF
CORS_ALLOWED_ORIGINS = [h.strip() for h in os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",") if h.strip()]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [h.strip() for h in os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",") if h.strip()]

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
    # 추가: allauth 미들웨어
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

# Database (기본: SQLite → 운영에서는 .env에서 override 권장)
db_engine = os.getenv("DB_ENGINE", "sqlite")  # 기본은 sqlite

if db_engine == "postgres":
    ENGINE = "django.db.backends.postgresql"
elif db_engine == "mysql":
    ENGINE = "django.db.backends.mysql"
else:
    ENGINE = "django.db.backends.sqlite3"

if ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": ENGINE,
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": ENGINE,
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }


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
}

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
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}