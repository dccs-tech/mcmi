# Generated by Django 2.1.3 on 2019-03-02 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20190224_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='environment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group_relation', to='environment.Environment'),
        ),
    ]