# Generated by Django 5.1.6 on 2025-02-25 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_app', '0003_alter_attendance_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='reg_no',
            new_name='registration_number',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent')], max_length=1),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance_app.student'),
        ),
    ]
