# Generated by Django 2.1.7 on 2019-06-04 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_group_admin_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='admin_id',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='groupmember',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='groupmember',
            old_name='member_id',
            new_name='member',
        ),
    ]
