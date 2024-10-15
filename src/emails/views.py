from django.shortcuts import render
from .forms import EmailForm
from django.conf import settings
from emails.models import Email, EmailVerificationEvent
from emails import services as email_services

# Retrieve email address from settings
EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def home_view(request, *args, **kwargs):
    template_name = "home.html"
    form = EmailForm(request.POST or None)  # Load form with POST data or None

    context = {
        "form": form,
        "message": "",
    }

    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = email_services.start_verification_event(email_val)
        print(obj)
        context["form"] = EmailForm()
        context["message"] = (
            f"Success! Check your email for verification from {EMAIL_ADDRESS}"
        )
    else:
        print(form.errors)
    return render(request, template_name, context)
