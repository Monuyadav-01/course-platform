from django import forms
from .models import Email, EmailVarificationEvent
from . import css, services


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email-login-input",
                "class": css.EMAIL_FIELD_CSS,
                "placeholder": "your email login",
            }
        )
    )

    class Meta:
        model = EmailVarificationEvent
        fields = ["email"]
