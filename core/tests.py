from django.test import TestCase
from django.urls import reverse


class CoreTemplateRoutesTests(TestCase):
    def test_new_template_routes_return_200(self):
        urls = [
            reverse('index'),
            reverse('projects'),
            reverse('project_detail', kwargs={'slug': 'lumina-storefront'}),
            reverse('project_detail', kwargs={'slug': 'apex-dashboard'}),
            reverse('project_detail', kwargs={'slug': 'devflow'}),
            reverse('project_detail', kwargs={'slug': 'crypto-wallet'}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
