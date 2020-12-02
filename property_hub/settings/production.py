import environ

from .base import *

env = environ.Env(DEBUG=(bool, False))

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

DATABASES = {"default": env.db()}

EMAIL_HOST_USER = env("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

CLOUDINARY_CLOUD_NAME = env("CLOUDINARY_CLOUD_NAME")

CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY")

CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET")

SENTRY = sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.7,
    send_default_pii=True,
)

CLOUDINARY = cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

HUEY = {
    "name": "property_hub",
    "url": env("REDIS_URL"),
}
