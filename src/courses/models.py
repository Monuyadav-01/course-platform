import uuid
import helpers._cloudinary as _cloudinary
import helpers
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Initialize Cloudinary
_cloudinary.cloudinary_init()


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
    if hasattr(instance, "path"):
        path = instance.path.strip("/")
        return path

    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)

    if not public_id:
        return model_name_slug.strip()

    return f"{model_name_slug}/{public_id}".strip()


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
    if hasattr(instance, "get_display_name"):
        return instance.get_display_name()
    elif hasattr(instance, "title"):
        return instance.title

    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"


#  get_thumbnail_display_name = lambda instance: get_display_name(
#     instance, is_thumbnail=True
# )


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=110, blank=True, null=True, db_index=True)
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

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title}  -- Course"

    # Check if course is published
    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED


# Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length=110, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        "image",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["image", "thumbnail", "lesson"],
        blank=True,
        null=True,
    )
    video = CloudinaryField(
        "video",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["video", "thumbnail", "lesson"],
        blank=True,
        type="private",
        null=True,
        resource_type="video",
    )
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

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/courses/{self.public_id}"

    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    def get_display_name(self):
        return f"{self.title}  - {self.course.get_display_name}"

    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.PUBLISHED

    @property
    def has_video(self):
        return self.video is not None
