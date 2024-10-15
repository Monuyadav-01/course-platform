from django.shortcuts import render
from django.http import HttpResponse

from . import services


def verify_email_token(request, token, *args, **kwargs):
    did_verify, msg = services.verify_token(token)
    if not did_verify:
        return HttpResponse(msg)
    return HttpResponse(token)
