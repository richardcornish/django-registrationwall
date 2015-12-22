"""
Settings for running app tests independent of inclusion in a Django project

"""


# Requred by Django, although we the database is unused
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'paywall',
)

# Also required by Django
SECRET_KEY = 'l33t!'
