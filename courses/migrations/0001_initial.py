# Generated by Django 4.2.17 on 2024-12-21 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('content_type', models.CharField(blank=True, choices=[('SCORM', 'SCORM'), ('Video', 'Video'), ('Document', 'Document')], help_text='The type of content for this course.', max_length=50, null=True)),
                ('content_file', models.FileField(blank=True, help_text='The file associated with this course (SCORM, Video, or Document).', null=True, upload_to='course_content/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SCORM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('launch_url', models.CharField(max_length=255)),
                ('version', models.CharField(default='SCORM 1.2', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(help_text='The course this SCORM package belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='scorm_packages', to='courses.course')),
            ],
        ),
    ]