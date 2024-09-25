import cloudinary
from decouple import config  # similar to os.environ.get()

# Corrected variable names
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_PUBLIC_API_KEY = config(
    "CLOUDINARY_PUBLIC_API_KEY", default="757413762491437"
)
CLOUDINARY_SECRET_API_KEY = config("CLOUDINARY_SECRET_API_KEY", default="")


def cloudinary_init():
    # Ensure API secret exists
    if not CLOUDINARY_SECRET_API_KEY:
        raise ValueError("Cloudinary API Secret Key is missing!")

    # Initialize Cloudinary configuration
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_PUBLIC_API_KEY,
        api_secret=CLOUDINARY_SECRET_API_KEY,  # API Secret
        secure=True,
    )
