from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# Development database
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# Local development
CORS_ALLOW_ALL_ORIGINS = False