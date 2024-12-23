from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('learner', 'Learner'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='learner',  # Default role
        help_text="Role of the user (e.g., admin, instructor, learner)."
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text="The branch this user belongs to."
    )
    language = models.CharField(
        max_length=10,
        default='en',
        help_text="Preferred language of the user."
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="Preferred timezone of the user."
    )
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",
        blank=True,
        help_text="Specific permissions for this user."
    )

    # Adding utility fields for better management
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether this user account is active."
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the user joined the system."
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
