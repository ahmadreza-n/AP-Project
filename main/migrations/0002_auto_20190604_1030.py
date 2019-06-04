# Generated by Django 2.1.7 on 2019-06-04 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='admin_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Account'),
        ),
        migrations.AlterField(
            model_name='groupaccount',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Account', to_field='account_id'),
        ),
        migrations.AlterField(
            model_name='groupaccount',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Group', to_field='group_id'),
        ),
    ]
