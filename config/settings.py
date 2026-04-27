import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY='dev'
DEBUG=True
ALLOWED_HOSTS=['*']
INSTALLED_APPS=[
	'django.contrib.admin',
	'django.contrib.contenttypes',
	'django.contrib.auth',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'api',
	'dashboard',
]
MIDDLEWARE=[
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF='config.urls'
TEMPLATES=[
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	}
]
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.getenv('DB_NAME'),'USER':os.getenv('DB_USER'),'PASSWORD':os.getenv('DB_PASSWORD'),'HOST':os.getenv('DB_HOST'),'PORT':5432}}
# Email config
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=os.getenv('EMAIL_HOST','smtp.gmail.com')
EMAIL_PORT=int(os.getenv('EMAIL_PORT','587'))
EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS','True')=='True'
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER','')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD','')
DEFAULT_FROM_EMAIL=os.getenv('DEFAULT_FROM_EMAIL','noreply@iot-dashboard.local')

#Időzóna beállítása
TIME_ZONE = 'Europe/Budapest'
USE_TZ = True   
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Static files (CSS, JavaScript, Images)
# Required for django.contrib.staticfiles and admin
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'