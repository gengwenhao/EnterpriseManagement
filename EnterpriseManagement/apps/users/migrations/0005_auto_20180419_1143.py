# Generated by Django 2.0.3 on 2018-04-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_message_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='邮箱'),
        ),
    ]
