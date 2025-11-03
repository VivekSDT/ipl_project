# Copy this file to settings_local.py and edit with your Postgres credentials

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ipl_db',
        'USER': 'ipl_user',
        'PASSWORD': 'ipl_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
