# Generated by Django 3.0.7 on 2020-06-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedatabase', '0007_movie_niconico_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteraccount',
            name='is_main',
            field=models.BooleanField(default=True, verbose_name='メインアカウント'),
        ),
    ]