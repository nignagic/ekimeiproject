# Generated by Django 3.0.7 on 2020-06-08 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moviedatabase', '0006_auto_20200608_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='niconico_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='moviedatabase.NiconicoAccount', verbose_name='投稿ニコニコアカウント'),
        ),
    ]
