from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse

from contact.models import Message


class ContactTemplateTests(TestCase):
    @patch('contact.forms.ContactForm.send_mail')
    def test_contact_form_valid_post(self, mocked_send_mail):
        response = self.client.post(
            reverse('contact_form'),
            data={
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Hello',
                'message': 'Message content',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
        mocked_send_mail.assert_called_once()

    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
