# from django.apps import apps
from django.db.models import Q
from .models import Course, PublishStatus, Lesson


def get_publish_courses():
    # Course = apps.get_model("courses", "Course")
    return Course.objects.filter(status=PublishStatus.PUBLISHED)


def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(status=PublishStatus.PUBLISHED, public_id=course_id)
    except:
        pass
    return obj


def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson_set.filter(
        course__status=PublishStatus.PUBLISHED,
        status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
    ).filter(Q(status=PublishStatus.PUBLISHED), Q(status=PublishStatus.COMING_SOON))
    return lessons


def get_lesson_detail(lesson_id=None, course_id=None):
    if lesson_id is None or course_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_id,
            course__status=PublishStatus.PUBLISHED,
            status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
            id=lesson_id,
        )
    except Exception as e:
        print("lesson detail", e)
    return obj
