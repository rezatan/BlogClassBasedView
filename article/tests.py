from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestLoginFormView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='writer1', password='wrtr1234')

    def test_login_form_view(self):
        response = self.client.post(reverse('login'), {'username': 'writer1', 'password': 'wrtr1234'})
        self.assertEqual(response.status_code, 302)
