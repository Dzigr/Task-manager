# Generated by Django 4.2.3 on 2023-07-13 18:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_tasklabelrelation_task_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 13, 18, 49, 36, 136709, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
