from django.shortcuts import render
from django.http import JsonResponse
from contact.forms import ContactForm
from contact.models import Message
from core.models import GeneralSetting, ImageSetting

def get_general_setting(parameter):
    try:
        obj = GeneralSetting.objects.get(name=parameter).parameter
    except:
        obj = ''

    return obj

def get_image_setting(parameter):
    try:
        obj = ImageSetting.objects.get(name=parameter).file
    except:
        obj = ''

    return obj
# Create your views here.
def layout(request):

    #Contact Infos
    contact_area_address = get_general_setting('contact_area_address')
    contact_area_address_under_info = get_general_setting('contact_area_address_underinfo')
    contact_area_phone = get_general_setting('contact_area_phone')
    contact_area_phone_under_info = get_general_setting('contact_area_phone_underinfo')
    contact_area_email = get_general_setting('contact_area_email')
    contact_area_email_under_info = get_general_setting('contact_area_email_underinfo')

    context = {
        'contact_area_address': contact_area_address,
        'contact_area_address_under_info': contact_area_address_under_info,
        'contact_area_phone': contact_area_phone,
        'contact_area_phone_under_info': contact_area_phone_under_info,
        'contact_area_email': contact_area_email,
        'contact_area_email_under_info': contact_area_email_under_info,

    }
    return context
def contact_form(request):

    if request.POST:
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            contact_form.send_mail()

            success = True
            message = 'Contact form sent successfully.'
        else:
            success = False
            message = 'Contact form is not valid.'
    else:
        success = False
        message = 'Request method is not valid.'

    context = {
        'success': success,
        'message': message,
    }
    return JsonResponse(context)


def contact(request):
    contact_form = ContactForm()
    context = {
        'contact_form': contact_form,
    }
    return render(request, 'contact.html', context)
