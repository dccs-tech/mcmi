# Generated by Django 2.1.3 on 2019-01-26 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20190126_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='firewallrule',
            name='_config',
            field=models.TextField(db_column='config', null=True),
        ),
    ]
