# Generated by Django 2.1.7 on 2019-06-10 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_groupmember_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordratio',
            name='ratio',
            field=models.IntegerField(default=0),
        ),
    ]