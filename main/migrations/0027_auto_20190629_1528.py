# Generated by Django 2.2.1 on 2019-06-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20190629_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, height_field=400, upload_to='main/static/img/profile_pictures', width_field=400),
        ),
    ]