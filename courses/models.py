from django.db import models
from users.models import Branch, CustomUser


def content_file_path(instance, filename):
    if isinstance(instance, Course):
        return f"course_content/{instance.id}/{filename}"
    elif isinstance(instance, SCORM):
        return f"course_content/scorm/{instance.course.id}/{filename}"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
        help_text="The branch this course belongs to."
    )
    instructor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructor_courses",
        limit_choices_to={"role": "instructor"},
        help_text="The instructor assigned to this course."
    )
    enrolled_users = models.ManyToManyField(
        CustomUser,
        related_name="enrolled_courses",
        blank=True,
        limit_choices_to={"role": "learner"},
        help_text="The learners enrolled in this course."
    )
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('SCORM', 'SCORM'),
            ('Video', 'Video'),
            ('Document', 'Document'),
        ],
        null=True,
        blank=True,
        help_text="The type of content for this course."
    )
    content_file = models.FileField(
        upload_to=content_file_path,
        null=True,
        blank=True,
        help_text="The file associated with this course (SCORM, Video, or Document)."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Course: {self.title} (Branch: {self.branch})"


class SCORM(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="scorms",
        help_text="The course this SCORM package belongs to."
    )
    launch_url = models.CharField(max_length=255)
    version = models.CharField(max_length=50, default="SCORM 1.2")
    runtime_tracking = models.JSONField(
        default=dict,
        blank=True,
        help_text="Tracks learner progress, scores, and completion status."
    )
    time_spent = models.DecimalField(
        max_digits=6,  # Allow larger values for total time
        decimal_places=2,
        default=0.0,
        help_text="Total time spent by the learner in hours."
    )
    completion_status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='not_started',
        help_text="The current completion status of the SCORM package."
    )
    score = models.IntegerField(
        null=True,
        blank=True,
        help_text="The score returned from the SCORM package (if applicable)."
    )
    last_accessed = models.DateTimeField(
        auto_now=True,
        help_text="The timestamp for the last access of the SCORM package."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'title')
        verbose_name = "SCORM Package"
        verbose_name_plural = "SCORM Packages"

    def __str__(self):
        return f"{self.title} ({self.version})"
