import os
from urllib.parse import urlencode


class BaseConfig:
    """
    Base configuration.

    Contains all the configuration that is shared between all environments.
    """

    # General
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    BUNDLES = [
        "qrt.site",
        "qrt.parser",
    ]
    EXTENSIONS = [
        "mongo",
        "cors",
        "session",
    ]

    # Database
    MONGODB_PROTOCOL = "mongodb+srv"
    MONGODB_USERNAME = os.getenv("QUART_MONGODB_USERNAME")
    MONGODB_PASSWORD = os.getenv("QUART_MONGODB_PASSWORD")
    MONGODB_HOST = os.getenv("QUART_MONGODB_HOST")
    MONGODB_DB = os.getenv("QUART_MONGODB_DB")
    MONGODB_PARAMETRS = {
        "retryWrites": "true",
        "w": "majority",
        "appName": MONGODB_DB,
    }

    MONGO_URI = f"{MONGODB_PROTOCOL}://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}/{MONGODB_DB}?{urlencode(MONGODB_PARAMETRS)}"

    # CORS
    CORS_ALLOW_ORIGIN = os.getenv("QUART_CORS_ALLOW_ORIGIN", "*")

    # Session
    SESSION_TYPE = "mongodb"
    SESSION_MONGODB_URI = MONGO_URI
    SESSION_MONGODB_COLLECTION = "sessions"
    SESSION_PROTECTION = True


class DevConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True


class TestConfig(BaseConfig):
    """Testing configuration"""

    DEBUG = True
    TESTING = True


class ProdConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
