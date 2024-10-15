from django.urls import path, include
from . import views

urlpatterns = [path("", views.verify_email_token)]
