from django.db import models


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "DRAFT"


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )

    access = models.CharField(
        max_length=10,
        choices=AccessRequirement.choices,
        default=AccessRequirement.ANYONE,
    )

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    # title
    # description
    # publish_date
    # image
    # access
    # status
