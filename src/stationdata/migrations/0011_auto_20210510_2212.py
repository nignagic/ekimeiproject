# Generated by Django 3.2.2 on 2021-05-10 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationdata', '0010_auto_20200611_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineservice',
            name='is_formal',
            field=models.CharField(blank=True, default=1, max_length=200, null=True, verbose_name='正式区間'),
        ),
        migrations.AlterField(
            model_name='lineservice',
            name='is_service',
            field=models.CharField(blank=True, default=1, max_length=200, null=True, verbose_name='運行系統'),
        ),
    ]
