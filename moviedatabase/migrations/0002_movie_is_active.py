# Generated by Django 3.0.2 on 2020-05-27 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedatabase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
