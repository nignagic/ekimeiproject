# Generated by Django 3.0.2 on 2020-06-05 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedatabase', '0004_auto_20200604_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(blank=True, verbose_name='日時')),
                ('category', models.CharField(blank=True, max_length=100, null=True, verbose_name='種類')),
                ('head', models.CharField(blank=True, max_length=100, null=True, verbose_name='概要')),
                ('text', models.TextField(blank=True, null=True, verbose_name='説明')),
            ],
        ),
    ]