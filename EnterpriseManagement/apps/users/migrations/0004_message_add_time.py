# Generated by Django 2.0.3 on 2018-03-27 15:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
