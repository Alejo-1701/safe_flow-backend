import os

os.environ["DATABASE_URL"] = "postgresql://unused:unused@localhost:5432/unused"
os.environ["SECRET_KEY"] = "clave-solo-para-tests"
os.environ["DEBUG"] = "True"
os.environ["ALLOWED_HOSTS"] = "localhost,127.0.0.1,testserver"
os.environ["CORS_ALLOW_ALL_ORIGINS"] = "False"

from config.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
