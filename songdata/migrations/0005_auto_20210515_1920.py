# Generated by Django 3.2.2 on 2021-05-15 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songdata', '0004_songnew'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songnew',
            name='artist_name',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='アーティスト名'),
        ),
        migrations.AlterField(
            model_name='songnew',
            name='artist_name_kana',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='アーティスト名カナ'),
        ),
        migrations.AlterField(
            model_name='songnew',
            name='tag',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='タグ'),
        ),
    ]