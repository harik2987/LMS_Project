# Generated by Django 4.2.17 on 2024-12-22 17:06

import courses.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorm',
            name='runtime_tracking',
            field=models.JSONField(blank=True, default=dict, help_text='Tracks learner progress, scores, and completion status.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='content_file',
            field=models.FileField(blank=True, help_text='The file associated with this course (SCORM, Video, or Document).', null=True, upload_to=courses.models.content_file_path),
        ),
        migrations.AlterField(
            model_name='scorm',
            name='course',
            field=models.ForeignKey(help_text='The course this SCORM package belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='scorms', to='courses.course'),
        ),
        migrations.AlterUniqueTogether(
            name='scorm',
            unique_together={('course', 'title')},
        ),
    ]