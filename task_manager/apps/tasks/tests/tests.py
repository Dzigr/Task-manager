from django.contrib.auth import get_user_model
from task_manager.apps.tasks.models import Task
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.json_data_reader import get_json_data
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class TaskTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']
    test_tasks = get_json_data('test_task')

    def setUp(self):
        self.client = Client()

        self.user_without_tasks = get_user_model().objects.get(pk=1)
        self.author = get_user_model().objects.get(pk=2)
        self.executor = get_user_model().objects.get(pk=3)

        self.task_1 = Task.objects.get(pk=30)
        self.task_2 = Task.objects.get(pk=31)

        self.tasks = Task.objects.all()
        self.tasks_count = Task.objects.count()
        self.tasks_pk = self.tasks.values_list('pk', flat=True)

        self.login_url = reverse('login')
        self.tasks_url = reverse('tasks')
        self.task_create_url = reverse('task_create')
        self.task_update_url = reverse(
            'task_update',
            args=[self.task_1.pk],
        )
        self.task_delete_url = reverse(
            'task_delete',
            args=[self.task_1.pk],
        )
        self.client.force_login(self.author)


class TaskListViewTestCase(TaskTestCase):
    def test_view(self):
        response = self.client.get(self.tasks_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/main.html')

        self.client.logout()
        response = self.client.get(self.tasks_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_content(self):
        response = self.client.get(self.tasks_url)
        tasks = response.context['tasks']

        self.assertEqual(len(tasks), self.tasks_count)
        self.assertQuerysetEqual(tasks, self.tasks, ordered=False)

    def test_links(self):
        self.client.force_login(self.author)
        response = self.client.get(self.tasks_url)

        for pk in self.tasks_pk:
            self.assertContains(response, '/tasks/{pk}/update/'.format(pk=pk))
            self.assertContains(response, '/tasks/{pk}/delete/'.format(pk=pk))

    def test_filter_form(self):
        response = self.client.get(
            self.tasks_url,
            {"status": self.task_2.status.pk},
        )
        tasks = Task.objects.filter(status=self.task_2.status.pk)

        self.assertQuerysetEqual(response.context['tasks'], tasks)

        response = self.client.get(
            self.tasks_url,
            {'user_task': 'on'},
        )
        tasks = Task.objects.filter(author=self.author)
        self.assertQuerysetEqual(response.context['tasks'], tasks)
        self.client.logout()
        self.client.force_login(self.user_without_tasks)
        response = self.client.get(
            self.tasks_url,
            {'user_task': 'on'},
        )
        self.assertQuerysetEqual(response.context['tasks'], [])


class TaskCreateViewTestCase(TaskTestCase):
    def test_view(self):
        response = self.client.get(self.task_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_add_valid_task(self):
        response = self.client.post(
            self.task_create_url,
            self.test_tasks['new_valid'],
        )
#
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.tasks_url)
        self.assertEquals(
            self.tasks_count + 1,
            Task.objects.count(),
        )
        self.assertEquals(
            Task.objects.last().name,
            self.test_tasks['new_valid']['name'],
        )

    def test_add_missing_name_task(self):
        response = self.client.post(
            self.task_create_url,
            self.test_tasks['new_not_valid'],
        )
        errors = response.context['form'].errors

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertIn('status' and 'name', errors)

    def test_add_existing_name_status(self):
        response = self.client.post(
            self.task_create_url,
            self.test_tasks['existing'],
        )
        errors = response.context['form'].errors

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertEqual(
            [_('Task with this Name already exists.')],
            errors['name']
        )


class TaskUpdateViewTestCase(TaskTestCase):
    def test_view(self):
        response = self.client.get(self.task_update_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

    def test_update_status(self):
        new_data = self.test_tasks['new_valid']

        response = self.client.post(
            self.task_update_url,
            new_data,
            follow=True,
        )

        self.assertEquals(
            Task.objects.get(pk=30).name,
            new_data['name'],
        )
        self.assertEquals(
            self.tasks_count,
            Task.objects.count(),
        )
        self.assertContains(
            response,
            text=_('Task successfully updated'),
        )


class TaskDeleteViewTestCase(TaskTestCase):
    def test_view(self):
        response = self.client.get(self.task_delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_delete_task(self):
        response = self.client.post(self.task_delete_url)

        self.assertRedirects(response, self.tasks_url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=30)
        self.assertEquals(
            Task.objects.count(),
            self.tasks_count - 1,
        )

    def test_delete_task_not_author(self):
        self.client.force_login(self.user_without_tasks)
        response = self.client.post(
            self.task_delete_url,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.tasks_url)
        self.assertEqual(Task.objects.count(), self.tasks_count)
        self.assertContains(
            response,
            text=_("A task can only be deleted by its author."),
        )
