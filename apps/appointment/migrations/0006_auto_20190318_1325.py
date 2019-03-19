# Generated by Django 2.1.7 on 2019-03-18 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_auto_20190318_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='token_no',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.Patient'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Confirmed'), (2, 'Cancelled'), (3, 'Waiting')], default=3, null=True),
        ),
    ]
