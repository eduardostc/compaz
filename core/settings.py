from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-erzsl2wgc=yq$b0q9z3t6a5&#=!r)y4f(nh%))%%u#+j2aoy^t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compaz',

    'django_bootstrap5',
    'chartjs', #app para geração dos graficos.
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

ROOT_URLCONF = 'core.urls'

import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'compaz/templates')],  # Adicione o caminho do seu app
        #'DIRS': [BASE_DIR / 'templates'],  # Adicione o diretório de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'compaz.context_processors.is_gerente_context', #Gerentes de Atendimento
                'compaz.context_processors.is_gestor_context', #Gestores de Relatórios
                'compaz.context_processors.pertence_grupo_exclusao_context',  # Grupo de Exclusão
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'parceiros_db',
#         'USER': 'postgres',
#         'PASSWORD': '@Admin123',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/' # Usado durante o desenvolvimento
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Diretório de arquivos estáticos durante o desenvolvimento
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Diretório de arquivos estáticos durante a produção
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Modelo personalizado
AUTH_USER_MODEL = 'compaz.CustomUsuario'

# settings.py coloca a 'Data do atendimento' no formato brasileiro
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',  # Formato brasileiro
    '%Y-%m-%d',  # Formato ISO (padrão do Django)
]

# Redireciona para a página de criação de atendimento após o login
# Configuração correta no settings.py
LOGIN_REDIRECT_URL = '/meus-atendimentos/'  # Após login, redireciona para "Meus Atendimentos"
LOGOUT_REDIRECT_URL = '/login/'  # Ou para qualquer outra página de sua escolha
LOGIN_URL = '/login/'  # URL que será usada para redirecionar usuários não autenticados


# Configurações de e-mail (para testes)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações de e-mail (para produção)
# Exemplo usando SMTP do Gmail:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'seu-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'sua-senha'
# DEFAUTL_FROM_EMAIL = 'contato@fusion.com.br'
# EMAIL_HOST_USER = 'no-reply@fusion.com.br'


#Ambiente de Desenvolvimento
SESSION_COOKIE_SECURE = False  # Permitir cookies em HTTP, já que o HTTPS pode não estar ativo.
CSRF_COOKIE_SECURE = False  # Permitir requisições CSRF sem HTTPS.
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']  # Origens confiáveis no ambiente de desenvolvimento.
SECURE_SSL_REDIRECT = False  # Não redirecionar para HTTPS.

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',  # Sem cache persistente.
    }
}

# Opcional (desabilitar medidas de segurança desnecessárias durante o desenvolvimento):
# SECURE_HSTS_SECONDS = 0  # Não habilitar cabeçalhos Strict-Transport-Security.
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_CONTENT_TYPE_NOSNIFF = False
# SECURE_BROWSER_XSS_FILTER = False
# X_FRAME_OPTIONS = 'SAMEORIGIN'  # Permitir o carregamento do site em um iframe no mesmo domínio.

#Ambiente de Produção
# SESSION_COOKIE_SECURE = True  # Apenas enviar cookies sobre HTTPS.
# CSRF_COOKIE_SECURE = True  # Apenas aceitar tokens CSRF enviados via HTTPS.
# CSRF_COOKIE_HTTPONLY = True  # Impedir acesso de JavaScript ao token CSRF.

# SECURE_HSTS_SECONDS = 31536000  # Habilitar Strict-Transport-Security por 1 ano.
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Aplicar HSTS a todos os subdomínios.
# SECURE_CONTENT_TYPE_NOSNIFF = True  # Evitar que navegadores tentem adivinhar o tipo de conteúdo.
# SECURE_BROWSER_XSS_FILTER = True  # Habilitar proteção contra ataques XSS no navegador.
# SECURE_SSL_REDIRECT = True  # Redirecionar todo o tráfego HTTP para HTTPS.

# X_FRAME_OPTIONS = 'DENY'  # Bloquear carregamento do site em iframes para evitar ataques de clickjacking.

# CSRF_TRUSTED_ORIGINS = ['https://www.sua_producao.com']  # Substitua pelo domínio do site em produção.

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # Use um cache apropriado para produção.
#     }
# }

SESSION_COOKIE_AGE = 1800  # 10 minutos (10 x 60 segundos)
SESSION_SAVE_EVERY_REQUEST = True # renova a validade a cada requisição
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Salva sessões no banco de dados
