from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    subject = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'})
    )

    def send_mail(self):
        if self.is_valid():
            name = self.cleaned_data.get('name')
            email = self.cleaned_data.get('email')
            subject = self.cleaned_data.get('subject')
            message = self.cleaned_data.get('message')
            message_content = f"Message received\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"

            #send email
            email = EmailMessage(
            subject,
            message_content,
            to=[settings.DEFAULT_FROM_EMAIL],
            reply_to=[email],
            )
            email.send()




