# Generated by Django 2.1.7 on 2019-04-06 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='timeslot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appointment.TimeSlot'),
        ),
    ]
