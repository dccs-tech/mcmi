# Generated by Django 2.2 on 2019-04-07 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='groups',
            field=models.ManyToManyField(related_name='module_relations', to='group.Group'),
        ),
    ]
