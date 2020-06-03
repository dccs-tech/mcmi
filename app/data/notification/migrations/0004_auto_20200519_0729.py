# Generated by Django 3.0 on 2020-05-19 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0002_auto_20190520_0649'),
        ('notification', '0003_auto_20200202_0749'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['name'], 'verbose_name': 'notification', 'verbose_name_plural': 'notifications'},
        ),
        migrations.AlterModelOptions(
            name='notificationfailuregroup',
            options={'ordering': ['id'], 'verbose_name': 'notification failure group', 'verbose_name_plural': 'notification failure groups'},
        ),
        migrations.AlterModelOptions(
            name='notificationgroup',
            options={'ordering': ['id'], 'verbose_name': 'notification group', 'verbose_name_plural': 'notification groups'},
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together={('environment', 'name')},
        ),
    ]