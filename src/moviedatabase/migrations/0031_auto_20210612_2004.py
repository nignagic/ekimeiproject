# Generated by Django 3.2.2 on 2021-06-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedatabase', '0030_auto_20210612_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-published_at']},
        ),
        migrations.AddField(
            model_name='part',
            name='complex_category',
            field=models.TextField(blank=True, verbose_name='複合カテゴリー'),
        ),
    ]
