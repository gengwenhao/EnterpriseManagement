# Generated by Django 2.0.3 on 2018-05-03 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180423_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['add_time'], 'verbose_name': '用户留言', 'verbose_name_plural': '用户留言'},
        ),
    ]
