# Generated by Django 4.2.7 on 2023-11-11 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_farmerprofile_managers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FarmerProfile',
            new_name='FarmerLandInformation',
        ),
    ]
