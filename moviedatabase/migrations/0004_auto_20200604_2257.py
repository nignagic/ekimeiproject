# Generated by Django 3.0.2 on 2020-06-04 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviedatabase', '0003_auto_20200528_0059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='vocal',
        ),
        migrations.RemoveField(
            model_name='part',
            name='vocal',
        ),
        migrations.DeleteModel(
            name='Vocal',
        ),
    ]
