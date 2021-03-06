# Generated by Django 3.0.2 on 2020-05-27 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songdata', '0003_vocalnew'),
        ('moviedatabase', '0002_movie_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='vocalnew',
            field=models.ManyToManyField(blank=True, to='songdata.VocalNew', verbose_name='使用ボーカル(動画全体)'),
        ),
        migrations.AddField(
            model_name='part',
            name='vocalnew',
            field=models.ManyToManyField(blank=True, to='songdata.VocalNew', verbose_name='使用ボーカル(パート)'),
        ),
    ]
