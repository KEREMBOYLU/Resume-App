from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def contact_form(request):
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        context = {
            'success': True,
            'message': 'Contact form sent successfully.',
        }

    else:
        context = {
            'success': False,
            'message': 'Request method is not valid.',
        }

    return  JsonResponse(context)

def contact(request):
    return render(request, 'contact.html')