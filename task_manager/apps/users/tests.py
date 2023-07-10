from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.main_url = reverse('main')
        self.login_url = reverse('login')
        self.users_url = reverse('users')
        self.user_create_url = reverse('create')

        self.credentials = {
            'first_name': 'Uri',
            'last_name': 'Gagarin',
            'username': 'Cosmo',
            'password': 'Vostok',
        }

        self.test_user = get_user_model().objects.create_user(**self.credentials)

        self.edit_user_url = reverse('edit', args=[self.test_user.id])
        self.delete_user_url = reverse('delete', args=[self.test_user.id])

    # def test_login(self):
    #     # send login data
    #     response = self.client.post(
    #         '/login/',
    #         {
    #             'username': 'Cosmo',
    #             'password': 'Vostok',
    #          },
    #         follow=True)
    #     self.assertTrue(response.context['user'].is_active)

    def login(self):
        user = get_user_model().objects.get(username=self.test_user.username)
        self.client.force_login(user)

    def test_homepage_GET(self):
        response = self.client.get(self.main_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/user_auth.html')

    def test_UserListView_GET(self):
        response = self.client.get(self.users_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/main.html')

    def test_UserCreateView_GET(self):
        response = self.client.get(self.user_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_UserUpdateView_GET(self):
        self.login()
        response = self.client.get(self.edit_user_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_UserDeleteView_GET(self):
        self.login()
        response = self.client.get(self.delete_user_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
