# Generated by Django 3.0.4 on 2020-04-07 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.URLField(blank=True, default='https://i.imgur.com/Gcw4VIN.png', null=True, verbose_name='Picture url'),
        ),
    ]
