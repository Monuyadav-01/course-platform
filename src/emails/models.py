from django.db import models


# Create your models here.
class Email(models.Model):
    email = models.EmailField(unique=True)
    timestamps = models.DateTimeField(auto_now_add=True)


class EmailVarificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    # Token

    expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    attempts = models.IntegerField(default=0)
    expired = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    expired_at = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    last_attemp_at = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    timestamps = models.DateTimeField(auto_now_add=True)
