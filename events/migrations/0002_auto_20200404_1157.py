# Generated by Django 3.0.4 on 2020-04-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_access_token',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='stripe_access_token'),
        ),
        migrations.AddField(
            model_name='profile',
            name='stripe_user_id',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='stripe_user_id'),
        ),
    ]