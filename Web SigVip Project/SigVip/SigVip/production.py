from .settings import *

DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grupo10',
        'USER': 'grupo10',
        'PASSWORD': '198896276',
        'DEFAULT-CHARACTER-SET': 'utf8',
        'HOST': 'grupo10.c5d4mi2dthpc.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'TEST': {
            'NAME': 'planificacion_test'
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

#ADMIN_ENABLED=False
DEBUG=False
SECRET_KEY=os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST=True
USE_X_FORWARDED_PORT=True