from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        "<slug:course_id>/lessons/<slug:lesson_id>/",
        views.lesson_detail_view,
    ),
    path("<slug:course_id>/", views.course_detail_view),  # Fixed this line
    path("", views.course_list_view),
]
