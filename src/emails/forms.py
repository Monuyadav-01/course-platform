from django import forms
from .models import Email

# from .models import Email, EmailVerificationEvent
from . import css


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email-login-input",
                "class": css.EMAIL_FIELD_CSS,
                "placeholder": "Enter your email",
            }
        )
    )

    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Email.objects.filter(email=email, active=False)
        print(qs)
        if not email.endswith("gmail.com"):
            raise forms.ValidationError("Invalid email , Please try again")
        return email
