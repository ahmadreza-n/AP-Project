# Generated by Django 2.2.1 on 2019-06-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20190629_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='main/static/img/profile_pictures'),
        ),
    ]
