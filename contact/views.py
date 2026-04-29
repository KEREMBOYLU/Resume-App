from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse
from contact.forms import ContactForm
from contact.models import Message


def contact_form(request):
    contact_form_obj = ContactForm(request.POST or None)
    wants_json = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('accept', '')
    )

    if request.method != 'POST':
        success = False
        message = 'Request method is not valid.'
    elif contact_form_obj.is_valid():
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
        success = False
        message = 'Contact form is not valid.'

    context = {
        'success': success,
        'message': message,
    }
    if wants_json:
        return JsonResponse(context)

    status = 'success' if success else 'error'
    return redirect(f"{reverse('contact')}?contact_status={status}")


def contact(request):
    context = {
        'contact_form': ContactForm(),
        'contact_status': request.GET.get('contact_status', ''),
    }
    return render(request, 'contact.html', context=context)
