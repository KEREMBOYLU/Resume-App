from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse
from contact.forms import ContactForm
from contact.models import Message


def verify_turnstile(request):
    token = request.POST.get('cf-turnstile-response', '')
    if not token:
        return False

    data = urlencode({
        'secret': settings.TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': request.META.get('REMOTE_ADDR', ''),
    }).encode()
    verification_request = Request(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        data=data,
        method='POST',
    )

    try:
        with urlopen(verification_request, timeout=5) as response:
            result = json.loads(response.read().decode())
    except Exception:
        return False

    return result.get('success') is True


def contact_form(request):
    contact_form_obj = ContactForm(request.POST or None)
    wants_json = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('accept', '')
    )

    if request.method != 'POST':
        success = False
        message = 'Request method is not valid.'
    else:
        form_is_valid = contact_form_obj.is_valid()
        turnstile_is_valid = verify_turnstile(request) if form_is_valid else False
        if form_is_valid and turnstile_is_valid:
            Message.objects.create(
                name=contact_form_obj.cleaned_data.get('name'),
                email=contact_form_obj.cleaned_data.get('email'),
                subject=contact_form_obj.cleaned_data.get('subject'),
                message=contact_form_obj.cleaned_data.get('message'),
            )
            contact_form_obj.send_mail()
            success = True
            message = 'Contact form sent successfully.'
        else:
            if form_is_valid and not turnstile_is_valid:
                contact_form_obj.add_error(None, 'Please complete the verification.')
            success = False
            message = 'Contact form is not valid.'

    context = {
        'success': success,
        'message': message,
        'errors': contact_form_obj.errors,
    }
    if wants_json:
        return JsonResponse(context)

    status = 'success' if success else 'error'
    if request.method == 'POST' and not success:
        context = {
            'contact_form': contact_form_obj,
            'contact_status': status,
            'turnstile_site_key': settings.TURNSTILE_SITE_KEY,
        }
        return render(request, 'contact.html', context=context)

    return redirect(f"{reverse('contact')}?contact_status={status}")


def contact(request):
    context = {
        'contact_form': ContactForm(),
        'contact_status': request.GET.get('contact_status', ''),
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY,
    }
    return render(request, 'contact.html', context=context)
