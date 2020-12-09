from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'planificacion',
        'USER' : 'icf',
        'PASSWORD' : 'root',
        'DEFAULT-CHARACTER-SET' : 'utf8',
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
        'TEST': {
            'NAME': 'planificacion_test',
        }
    },
}