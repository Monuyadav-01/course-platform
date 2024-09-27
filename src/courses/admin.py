from django.contrib import admin
from django.utils.html import format_html
from cloudinary import CloudinaryImage

# Register your models here.
from .models import Course, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["public_id", "title", "status", "access"]
    list_filter = ["public_id", "status", "access"]
    fields = [
        "public_id",
        "title",
        "description",
        "status",
        "image",
        "access",
        "display_image",
    ]
    readonly_fields = ["display_image", "public_id"]

    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin_url

        return format_html(f"<img src = {url} />")

    display_image.short_description = "Current image"
