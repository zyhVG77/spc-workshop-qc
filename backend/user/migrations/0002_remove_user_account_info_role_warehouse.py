# Generated by Django 3.2.5 on 2022-04-26 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_account_info',
            name='role_warehouse',
        ),
    ]
