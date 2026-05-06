from django import forms
from django.core.mail import EmailMessage
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField(
        min_length=2,
        max_length=80,
        required=True,
        error_messages={
            'required': 'Name is required.',
            'min_length': 'Name must be at least 2 characters.',
            'max_length': 'Name must be at most 80 characters.',
        },
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        },
    )
    subject = forms.CharField(
        min_length=3,
        max_length=120,
        required=True,
        error_messages={
            'required': 'Subject is required.',
            'min_length': 'Subject must be at least 3 characters.',
            'max_length': 'Subject must be at most 120 characters.',
        },
    )
    message = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        max_length=2000,
        required=True,
        error_messages={
            'required': 'Message is required.',
            'min_length': 'Message must be at least 10 characters.',
            'max_length': 'Message must be at most 2000 characters.',
        },
    )

    def send_mail(self):
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        subject = self.cleaned_data.get('subject')
        message = self.cleaned_data.get('message')
        message_context = 'Message received. \n\n' \
                          'Name: %s\n' \
                          'Subject: %s\n' \
                          'Email: %s\n' \
                          'Message: %s\n' % (name, subject, email, message)

        # send email
        email = EmailMessage(
            subject,
            message_context,
            to=[settings.DEFAULT_RECEIVER_EMAIL],
            reply_to=[email],
        )
        email.send()
