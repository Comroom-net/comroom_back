from .base import *


DEBUG = True

WEB_URL = "http://dev.comroom.net/"

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://dev.comroom.net",
    "http://comroom.net",
]
