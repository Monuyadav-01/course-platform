from django.contrib import admin
from django.utils.html import format_html
from cloudinary import CloudinaryImage

# Register your models here.
from .models import Course, Lesson
import helpers


class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = ["public_id", "updated", "display_image", "display_vieo"]
    extra = 0

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj, field_name="thumbnail", width=200
        )

        return format_html(f"<img src = {url} />")

    display_image.short_description = "Current image"

    def display_vieo(self, obj, *args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            obj, field_name="video", as_html=True, width=550
        )

        return video_embed_html

    display_vieo.short_description = "Current Video"


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
        url = helpers.get_cloudinary_image_object(obj, field_name="image", width=200)

        return format_html(f"<img src = {url} />")

    display_image.short_description = "Current image"
