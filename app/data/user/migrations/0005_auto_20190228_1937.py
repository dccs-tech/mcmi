# Generated by Django 2.1.3 on 2019-03-01 00:37

import data.user.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190225_1204'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', data.user.models.UserManager()),
            ],
        ),
    ]
