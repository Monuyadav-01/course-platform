import uuid
import helpers
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Initialize Cloudinary
helpers.cloudinary_init()


# Choices for Access Requirement and Publish Status
class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "DRAFT"


def handle_upload(instance, filename):
    # Include unique identifier in the path for file uploads
    return f"courses/{instance.id or uuid.uuid4().hex[:5]}/{filename}"


# Generate public ID prefix for Cloudinary fields
def get_public_id_prefix(instance, *args, **kwargs):
    public_id = instance.public_id
    if not public_id:
        return "courses"
    return "Courses Uploaded"


# Generate unique public ID for a course
def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    return f"{slug}--{unique_id[:5]}"


# Get display name for Cloudinary uploads
def get_display_name(instance, *args, **kwargs):
    return instance.title or "Course Upload"


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=110, blank=True, null=True)
    image = CloudinaryField(
        "image",
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course", "thumbnail"],
    )
    status = models.CharField(
        max_length=15,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )
    access = models.CharField(
        max_length=15,
        choices=AccessRequirement.choices,
        default=AccessRequirement.ANYONE,
    )

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    # Check if course is published
    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    # Generate admin URL for course image with Cloudinary
    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        image_options = {"width": 200}
        return self.image.build_url(**image_options)

    # Return course image detail URL or HTML, with customizable width
    @property
    def git_image_detail(self, as_html=False, width=750):
        if not self.image:
            return ""
        image_options = {"width": width}
        if as_html:
            return self.image.image(**image_options)
        return self.image.build_url(**image_options)


# Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(
        default=False,
        help_text="If user does not have access to course, can they see this",
    )
    status = models.CharField(
        max_length=15,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-updated"]

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
