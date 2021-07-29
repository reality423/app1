"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR의 기본 경로는 해당 프로젝트의 ROOT 경로
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# django의 각종 쿠키 파일관리등 보안을 담당하는 key
# 시크릿키 노출시 해당 jango 프로젝트의 보안기능 상실 위험성 증가.
SECRET_KEY = '9#h3&822+x#1y2+yz-kcs*jsny_(^*fp7v)qf7^_^fbjp#4@vo'

# SECURITY WARNING: don't run with debug turned on in production!
# jango 프로젝트에 대한 log를 남길지 말지를 설정하는 부분.
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# 생성한 app들을 등록해주는 설정
# app1만 적혀 있다면 app1 __init__.py에서 default app config가 정의되어있는가를 확인
INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'app1.apps.App1Config',
    'django.contrib.admin',   # 관리자 #
    'django.contrib.auth',    # 권한 #
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # 로그인 상태 컨트롤
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # BASE_DIR = c:\projects\jango1
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DBMS mysql 변경
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crawl_data',
        'USER': 'crawl_user',
        'PASSWORD': '1234',
        'HOST' : 'localhost',
        'PORT' : '3306',
        'OPTIONS' : {
            'init_command' : 'SET sql_mode="STRICT_TRANS_TABLES"',
            'charset':'UTF8',
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# 언어 및 지역시간 설정

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
#

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'