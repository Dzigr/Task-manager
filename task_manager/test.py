from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class MainAuthTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('main')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        self.credentials = {
                'username': 'Beta',
                'password': 'some_p@ssword',
            }

        self.user = get_user_model().objects.create_user(**self.credentials)


class MainPageTestCase(MainAuthTestCase):
    def test_index_view(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')


class LoginLogoutTestCase(MainAuthTestCase):
    def test_login_view(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/user_auth.html')

    def test_login(self):
        test_login = self.client.login(**self.credentials)
        self.assertTrue(test_login)
        self.client.logout()

        response = self.client.post(
            self.login_url,
            self.credentials,
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.index_url)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        response = self.client.post(self.logout_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
