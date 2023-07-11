from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.json_data_reader import get_json_data
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class UserTestCase(TestCase):
    fixtures = ['users.json']
    test_user = get_json_data('test_user')

    def setUp(self):
        self.client = Client()

        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user3 = get_user_model().objects.get(pk=3)

        self.users = get_user_model().objects.all()
        self.users_count = get_user_model().objects.count()
        self.users_pk = self.users.values_list('pk', flat=True)

        self.users_url = reverse('users')
        self.user_create_url = reverse('create')
        self.login_url = reverse('login')
        self.user_edit_url = reverse(
            'edit',
            args=[self.user1.pk],
        )
        self.user_delete_url = reverse(
            'delete',
            args=[self.user1.pk],
        )


class UserListViewTestCase(UserTestCase):

    def test_view(self):
        response = self.client.get(self.users_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/main.html')

    def test_content(self):
        response = self.client.get(self.users_url)
        users = response.context['users']

        self.assertEqual(len(users), self.users_count)
        self.assertQuerysetEqual(users, self.users, ordered=False)

    def test_links(self):
        response = self.client.get(self.users_url)

        for pk in self.users_pk:
            self.assertContains(response, '/users/{pk}/update/'.format(pk=pk))
            self.assertContains(response, '/users/{pk}/delete/'.format(pk=pk))


class UserCreateViewTestCase(UserTestCase):
    def test_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.user_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_register_valid_user(self):
        response = self.client.post(
            self.user_create_url,
            self.test_user['new_valid'],
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertEquals(
            self.users_count + 1,
            get_user_model().objects.count(),
        )

    def test_register_not_valid_user(self):
        response = self.client.post(
            self.user_create_url,
            self.test_user['new_not_valid'],
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertContains(
            response,
            text=_('Unsuccessful registration. Invalid information.'),
        )


class UserUpdateViewTestCase(UserTestCase):
    def test_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.user_edit_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_update_user(self):
        self.client.force_login(self.user1)
        new_data = self.test_user['new_valid']

        response = self.client.post(
            self.user_edit_url,
            new_data,
            follow=True,
        )

        self.assertEquals(
            get_user_model().objects.get(pk=1).username,
            new_data['username'],
        )
        self.assertEquals(
            self.users_count,
            get_user_model().objects.count(),
        )
        self.assertContains(
            response,
            text=_('User information successfully updated'),
        )

    def test_update_without_permission(self):
        self.client.force_login(self.user2)

        new_data = self.test_user['new_valid']
        response = self.client.post(
            self.user_edit_url,
            new_data,
            follow=True,
        )

        self.assertRedirects(response, self.users_url)
        self.assertEquals(
            self.user1.username,
            get_user_model().objects.get(pk=1).username,
        )
        self.assertContains(
            response,
            text=_('You have no rights to change another user.'),
        )


class UserDeleteViewTestCase(UserTestCase):
    def test_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.user_delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_delete_user(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.user_delete_url)

        self.assertRedirects(response, self.users_url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(pk=1)
        self.assertEquals(
            get_user_model().objects.count(),
            self.users_count - 1,
        )

    def test_delete_without_permission(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.user_delete_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.users_url)
        self.assertContains(
            response,
            text=_('You have no rights to change another user.'),
        )
