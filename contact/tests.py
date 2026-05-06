from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse

from contact.models import Message


class ContactTemplateTests(TestCase):
    def valid_contact_data(self, **overrides):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Hello',
            'message': 'Message content',
        }
        data.update(overrides)
        return data

    @patch('contact.forms.ContactForm.send_mail')
    @patch('contact.views.verify_turnstile', return_value=True)
    def test_contact_form_valid_post(self, mocked_verify_turnstile, mocked_send_mail):
        response = self.client.post(
            reverse('contact_form'),
            data=self.valid_contact_data(),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
        mocked_verify_turnstile.assert_called_once()
        mocked_send_mail.assert_called_once()

    @patch('contact.forms.ContactForm.send_mail')
    def test_contact_form_rejects_empty_required_fields(self, mocked_send_mail):
        response = self.client.post(
            reverse('contact_form'),
            data={
                'name': '',
                'email': '',
                'subject': '',
                'message': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 0)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="subject"')
        self.assertContains(response, 'name="message"')
        self.assertContains(response, 'required')
        mocked_send_mail.assert_not_called()

    @patch('contact.forms.ContactForm.send_mail')
    def test_contact_form_rejects_invalid_field_lengths_and_email(self, mocked_send_mail):
        invalid_cases = [
            {'name': 'A'},
            {'name': 'A' * 81},
            {'email': 'not-an-email'},
            {'subject': 'Hi'},
            {'subject': 'A' * 121},
            {'message': 'Too short'},
            {'message': 'A' * 2001},
        ]

        for invalid_data in invalid_cases:
            with self.subTest(invalid_data=invalid_data):
                response = self.client.post(
                    reverse('contact_form'),
                    data=self.valid_contact_data(**invalid_data),
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(Message.objects.count(), 0)

        mocked_send_mail.assert_not_called()

    @patch('contact.forms.ContactForm.send_mail')
    def test_contact_form_uses_native_field_validation_markup(self, mocked_send_mail):
        response = self.client.post(
            reverse('contact_form'),
            data=self.valid_contact_data(message='d'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'minlength="10"')
        self.assertNotContains(response, 'Message must be at least 10 characters.')
        self.assertNotContains(response, 'fa-circle-exclamation')
        self.assertEqual(Message.objects.count(), 0)
        mocked_send_mail.assert_not_called()

    @patch('contact.forms.ContactForm.send_mail')
    @patch('contact.views.verify_turnstile', return_value=False)
    def test_contact_form_rejects_failed_turnstile(self, mocked_verify_turnstile, mocked_send_mail):
        response = self.client.post(
            reverse('contact_form'),
            data=self.valid_contact_data(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 0)
        self.assertContains(response, 'Please complete the verification.')
        mocked_verify_turnstile.assert_called_once()
        mocked_send_mail.assert_not_called()

    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cf-turnstile')
