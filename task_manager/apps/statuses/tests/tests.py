from django.contrib.auth import get_user_model
from task_manager.apps.statuses.models import Status
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.json_data_reader import get_json_data
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class StatusTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']
    test_statuses = get_json_data('test_status')

    def setUp(self):
        self.client = Client()

        self.user1 = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user1)

        self.status_1 = Status.objects.get(pk=10)
        self.status_2 = Status.objects.get(pk=11)

        self.statuses = Status.objects.all()
        self.statuses_count = Status.objects.count()
        self.statuses_pk = self.statuses.values_list('pk', flat=True)

        self.login_url = reverse('login')
        self.statuses_url = reverse('statuses')
        self.statuses_create_url = reverse('status_create')
        self.statuses_update_url = reverse(
            'status_update',
            args=[self.status_1.pk],
        )
        self.statuses_delete_url = reverse(
            'status_delete',
            args=[self.status_1.pk],
        )
        self.bound_status_delete_url = reverse(
            'status_delete',
            args=[self.status_2.pk],
        )


class StatusListViewTestCase(StatusTestCase):

    def test_view(self):
        response = self.client.get(self.statuses_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/main.html')

        self.client.logout()
        response = self.client.get(self.statuses_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_content(self):
        response = self.client.get(self.statuses_url)
        statuses = response.context['statuses']

        self.assertEqual(len(statuses), self.statuses_count)
        self.assertQuerysetEqual(statuses, self.statuses, ordered=False)

    def test_links(self):
        response = self.client.get(self.statuses_url)

        for pk in self.statuses_pk:
            self.assertContains(response, '/statuses/{pk}/update/'.format(pk=pk))
            self.assertContains(response, '/statuses/{pk}/delete/'.format(pk=pk))


class StatusCreateViewTestCase(StatusTestCase):
    def test_view(self):
        response = self.client.get(self.statuses_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

    def test_add_valid_status(self):
        response = self.client.post(
            self.statuses_create_url,
            self.test_statuses['new_valid'],
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.statuses_url)
        self.assertEquals(
            self.statuses_count + 1,
            Status.objects.count(),
        )

    def test_add_missing_name_status(self):
        response = self.client.post(
            self.statuses_create_url,
            self.test_statuses['new_not_valid'],
        )
        errors = response.context['form'].errors

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertEqual(
            [_('This field is required.')],
            errors['name']
        )

    def test_add_existing_name_status(self):
        response = self.client.post(
            self.statuses_create_url,
            self.test_statuses['existing'],
        )
        errors = response.context['form'].errors

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertEqual(
            [_('Status with this Name already exists.')],
            errors['name']
        )


class StatusUpdateViewTestCase(StatusTestCase):
    def test_view(self):
        response = self.client.get(self.statuses_update_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_update_status(self):
        new_data = self.test_statuses['new_valid']

        response = self.client.post(
            self.statuses_update_url,
            new_data,
            follow=True,
        )

        self.assertEquals(
            Status.objects.get(pk=10).name,
            new_data['name'],
        )
        self.assertEquals(
            self.statuses_count,
            Status.objects.count(),
        )
        self.assertContains(
            response,
            text=_('Status successfully updated'),
        )


class StatusDeleteViewTestCase(StatusTestCase):
    def test_view(self):
        response = self.client.get(self.statuses_delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_delete_user(self):
        response = self.client.post(self.statuses_delete_url)

        self.assertRedirects(response, self.statuses_url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=10)
        self.assertEquals(
            Status.objects.count(),
            self.statuses_count - 1,
        )

    def test_delete_bounded_status(self):
        response = self.client.post(
            self.bound_status_delete_url,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.statuses_url)
        self.assertEqual(Status.objects.count(), self.statuses_count)
        self.assertContains(
            response,
            text=_("Unable to delete status because it's in use"),
        )
