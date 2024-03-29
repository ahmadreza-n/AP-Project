# Generated by Django 2.1.7 on 2019-06-09 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_record_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordCoefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient', models.IntegerField()),
                ('member_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Account')),
            ],
        ),
        migrations.AlterField(
            model_name='group',
            name='admin_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Account'),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='group_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Group'),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='member_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Account'),
        ),
        migrations.AlterField(
            model_name='record',
            name='payer_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer_fk_name', to='main.Account'),
        ),
        migrations.AddField(
            model_name='recordcoefficient',
            name='record_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Group'),
        ),
    ]
