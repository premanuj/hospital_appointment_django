# Generated by Django 2.1.7 on 2019-03-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_auto_20190316_2032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='availablity',
            options={'verbose_name_plural': 'availablilities'},
        ),
        migrations.AlterField(
            model_name='availablity',
            name='time_slot',
            field=models.ManyToManyField(related_name='available', through='appointment.AvailableTime', to='appointment.TimeSlot'),
        ),
    ]