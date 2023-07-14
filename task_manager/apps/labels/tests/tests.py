from django.contrib.auth import get_user_model
from task_manager.apps.labels.models import Label
from django import test
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.json_data_reader import get_json_data
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class LabelTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']
    test_labels = get_json_data('test_label')

    def setUp(self):
        self.client = Client()

        self.user1 = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user1)

        self.label_1 = Label.objects.get(pk=50)
        self.label_2 = Label.objects.get(pk=51)
        self.label_3 = Label.objects.get(pk=52)

        self.labels = Label.objects.all()
        self.labels_count = Label.objects.count()
        self.labels_pk = self.labels.values_list('pk', flat=True)

        self.login_url = reverse('login')
        self.labels_url = reverse('labels')
        self.label_create_url = reverse('label_create')
        self.label_update_url = reverse(
            'label_update',
            args=[self.label_2.pk],
        )
        self.label_delete_url = reverse(
            'label_delete',
            args=[self.label_3.pk],
        )
        self.bound_label_delete_url = reverse(
            'label_delete',
            args=[self.label_1.pk],
        )


class LabelListViewTestCase(LabelTestCase):

    def test_view(self):
        response = self.client.get(self.labels_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/main.html')

        self.client.logout()
        response = self.client.get(self.labels_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_content(self):
        response = self.client.get(self.labels_url)
        labels = response.context['labels']

        self.assertEqual(len(labels), self.labels_count)
        self.assertQuerysetEqual(labels, self.labels, ordered=False)

    def test_links(self):
        response = self.client.get(self.labels_url)

        for pk in self.labels_pk:
            self.assertContains(response, '/labels/{pk}/update/'.format(pk=pk))
            self.assertContains(response, '/labels/{pk}/delete/'.format(pk=pk))


class LabelCreateViewTestCase(LabelTestCase):
    def test_view(self):
        response = self.client.get(self.label_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

    def test_add_valid_status(self):
        response = self.client.post(
            self.label_create_url,
            self.test_labels['new_valid'],
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)
        self.assertEquals(
            self.labels_count + 1,
            Label.objects.count(),
        )

    def test_add_missing_name_label(self):
        response = self.client.post(
            self.label_create_url,
            self.test_labels['new_not_valid'],
        )
        errors = response.context['form'].errors

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')
        self.assertEqual(
            [_('This field is required.')],
            errors['name']
        )

    def test_add_existing_name_label(self):
        response = self.client.post(
            self.label_create_url,
            self.test_labels['existing'],
        )
        errors = response.context['form'].errors

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')
        self.assertEqual(
            [_('Label with this Name already exists.')],
            errors['name']
        )


class LabelUpdateViewTestCase(LabelTestCase):
    def test_view(self):
        response = self.client.get(self.label_update_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

    def test_update_status(self):
        new_data = self.test_labels['new_valid']

        response = self.client.post(
            self.label_update_url,
            new_data,
            follow=True,
        )

        self.assertEquals(
            Label.objects.get(pk=51).name,
            new_data['name'],
        )
        self.assertEquals(
            self.labels_count,
            Label.objects.count(),
        )
        self.assertContains(
            response,
            text=_('Label successfully updated'),
        )


class LabelDeleteViewTestCase(LabelTestCase):
    def test_view(self):
        response = self.client.get(self.label_delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

    def test_delete_user(self):
        response = self.client.post(self.label_delete_url)

        self.assertRedirects(response, self.labels_url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=52)
        self.assertEquals(
            Label.objects.count(),
            self.labels_count - 1,
        )

    def test_delete_bounded_label(self):
        response = self.client.post(
            self.bound_label_delete_url,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.labels_url)
        self.assertEqual(Label.objects.count(), self.labels_count)
        self.assertContains(
            response,
            text=_("Unable to delete label because it's in use"),
        )
