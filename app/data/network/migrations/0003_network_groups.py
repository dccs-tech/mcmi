# Generated by Django 2.1.3 on 2019-03-01 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20190224_1023'),
        ('network', '0002_auto_20190224_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='groups',
            field=models.ManyToManyField(related_name='_network_groups_+', to='group.Group'),
        ),
    ]
