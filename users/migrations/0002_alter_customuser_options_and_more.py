# Generated by Django 4.2.17 on 2024-12-21 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-date_joined'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time the user joined the system.'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Indicates whether this user account is active.'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('superadmin', 'SuperAdmin'), ('admin', 'Admin'), ('instructor', 'Instructor'), ('learner', 'Learner')], default='learner', help_text='Role of the user (e.g., admin, instructor, learner).', max_length=20),
        ),
    ]