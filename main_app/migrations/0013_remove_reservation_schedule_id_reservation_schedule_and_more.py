# Generated by Django 4.2.7 on 2023-12-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_reservation_equipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='schedule_id',
        ),
        migrations.AddField(
            model_name='reservation',
            name='schedule',
            field=models.DateField(help_text='Required, select schedule here. If empty no available schedule.', null=True),
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
