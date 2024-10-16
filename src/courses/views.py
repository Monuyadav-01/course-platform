from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from . import services
import helpers


def course_list_view(request):
    queryset = services.get_publish_courses()
    print(queryset)
    context = {"object_list": queryset}
    # return JsonResponse({"data": [x.id for x in queryset]})
    return render(request, "courses/list.html", context)


def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_obj)
    context = {"course": course_obj, "lessons_queryset": lessons_queryset}
    return render(request, "courses/detail.html", context)


def lesson_detail_view(request, lesson_id=None, course_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(lesson_id=lesson_id, course_id=course_id)
    if lesson_obj is None:
        raise Http404
    # template_name = "courses/purchase-required.html"
    email_id_exists = request.session.get("email_id")
    if lesson_obj.requires_email and not email_id_exists:
        request.session["next_url"] = request.path
        return render(request, "courses/email-required.html", {})
    template_name = "courses/lesson-coming-soon.html"
    context = {"object": lesson_obj}
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        """
        Lesson is published,
        Video is available,
        go forward
        """
        template_name = "courses/lesson.html"
        video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj, field_name="video", as_html=True, width=1250
        )
        context["video_embed"] = video_embed_html
    return render(request, template_name, context)
