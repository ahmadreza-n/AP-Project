# Generated by Django 2.2.1 on 2019-06-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20190629_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_picture',
            field=models.ImageField(blank=True, upload_to='main/static/img/group_pictures'),
        ),
    ]