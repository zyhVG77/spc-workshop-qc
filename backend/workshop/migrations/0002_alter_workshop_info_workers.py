# Generated by Django 3.2.5 on 2021-08-02 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop_info',
            name='workers',
            field=models.ManyToManyField(help_text='可见用户', related_name='workshops', to='user.user_account_info'),
        ),
    ]
