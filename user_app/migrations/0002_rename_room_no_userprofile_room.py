# Generated by Django 5.1.6 on 2025-03-01 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='room_no',
            new_name='room',
        ),
    ]
