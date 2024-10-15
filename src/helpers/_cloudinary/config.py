import cloudinary
from decouple import config
from django.conf import settings

# Corrected variable names
CLOUDINARY_CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
CLOUDINARY_PUBLIC_API_KEY = settings.CLOUDINARY_PUBLIC_API_KEY
CLOUDINARY_SECRET_API_KEY = settings.CLOUDINARY_SECRET_API_KEY


def cloudinary_init():

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_PUBLIC_API_KEY,
        api_secret=CLOUDINARY_SECRET_API_KEY,  # API Secret
        secure=True,
    )
