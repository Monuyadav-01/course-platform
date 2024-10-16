from django.conf import settings
from django.core.mail import send_mail
from .models import Email, EmailVerificationEvent
from django.utils import timezone

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()


def get_verification_email_msg(verification_instance, as_html=False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    verify_link = verification_instance.get_link()
    if as_html:
        f"Verify your email with the following <h1> <p> <a href  = '{verify_link}'</a></p> </h1> "
    return f" Verify your email with the following:\n {verify_link}"


def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(parent=email_obj, email=email)
    sent = send_verification_email(obj.id)
    return obj, sent


def send_verification_email(verify_obj_id):
    verify_obj = EmailVerificationEvent.objects.get(id=verify_obj_id)
    email = verify_obj.email
    subject = "Verify your email"
    text_msg = get_verification_email_msg(verify_obj, as_html=False)
    text_html = get_verification_email_msg(verify_obj, as_html=True)
    from_user_email_addr = EMAIL_HOST_USER
    to_user_email = email
    return send_mail(
        subject,
        text_msg,
        from_user_email_addr,
        [to_user_email],
        fail_silently=False,
        html_message=text_html,
    )


def verify_token(token, max_attempts=5):
    qs = EmailVerificationEvent.objects.filter(token=token)
    if not qs.exists():
        return False, "Invalid token", None  # Return three values

    has_email_expired = qs.filter(expired=True)
    if has_email_expired.exists():
        """token expired"""
        return False, "Token expired, try again", None  # Return three values

    max_attempts_reached = qs.filter(attempts__gte=max_attempts)
    if max_attempts_reached.exists():
        """Update max attempts + 1"""
        return False, "Token expired, used too many times", None  # Return three values

    """Token Valid"""
    obj = qs.first()
    obj.attempts += 1
    obj.last_attemp_at = timezone.now()
    if obj.attempts > max_attempts:
        """Invalidation process"""
        obj.expired = True
        obj.expired_at = timezone.now()

    obj.save()
    email_obj = obj.parent  # Email object

    return True, "Welcome", email_obj  # Return three values when valid
