from pathlib import Path
# Añade esto al inicio
import os 
from dotenv import load_dotenv # Lo usaremos para cargar el SECRET_KEY localmente

# Cargar variables de entorno (opcional si usas un archivo .env, pero buena práctica)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vn@3(@c$q4cf@9vbl!b=vobnx1_n_60%%qz92es7rj=h3f47p9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    
    # TERCEROS
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular', # Documentación

    # APPS PROPIAS (De momento vacías)
    # Aquí iremos añadiendo nuestros módulos
    # ...RECEPCIÓN
    'core',
    'users', 
    'habitaciones', 
    'huespedes',
    'reservas',
    'recepcion',
    'cuentas',
    
    # ...RRHH
    'personal',
    'nomina',
    
    # ...INVENTARIO
    'inventario',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------------------------------
# CONFIGURACIÓN DE SEGURIDAD Y API
# ----------------------------------------------------

# 1. Definimos la app donde estará nuestro modelo de usuario (la crearemos luego)
AUTH_USER_MODEL = 'users.CustomUser' # ¡IMPORTANTE!

# 2. Configuramos el REST Framework para usar JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Usaremos la documentación de drf-spectacular
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# 3. Configuramos la documentación
SPECTACULAR_SETTINGS = {
    'TITLE': 'API Hotel Management System',
    'DESCRIPTION': 'Documentación de la API del sistema de gestión del hotel.',
    'VERSION': '1.0.0',
}

# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key-local-dev-only') # Lee de ENV
DEBUG = os.environ.get('DEBUG', 'True') == 'True' 
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') # Permite cualquier host dentro de Docker

# Configuración de Base de Datos (Reemplaza la configuración de SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'hoteldjdb'),
        'USER': os.environ.get('DB_USER', 'hoteldjuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'supersecurepassword'),
        'HOST': os.environ.get('DB_HOST', 'db'), # ¡CRUCIAL! 'db' es el nombre del servicio en docker-compose
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# config/settings.py (Añadir al final del archivo)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # La URL donde corre tu frontend
    "http://127.0.0.1:5173", # La versión 127.0.0.1
]

# Si necesitas permitir todos los métodos HTTP, asegúrate de que estos sean True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]