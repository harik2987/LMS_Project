from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class DashboardAccessTestCase(TestCase):
    def setUp(self):
        # Create users for each role
        self.superadmin = CustomUser.objects.create_superuser(username='superadmin', password='password', role='SuperAdmin')
        self.admin = CustomUser.objects.create_user(username='admin', password='password', role='Admin')
        self.instructor = CustomUser.objects.create_user(username='instructor', password='password', role='Instructor')
        self.learner = CustomUser.objects.create_user(username='learner', password='password', role='Learner')

    def test_superadmin_dashboard(self):
        self.client.login(username='superadmin', password='password')
        response = self.client.get(reverse('dashboard_superadmin'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('dashboard_admin'))
        self.assertEqual(response.status_code, 200)

    def test_instructor_dashboard(self):
        self.client.login(username='instructor', password='password')
        response = self.client.get(reverse('dashboard_instructor'))
        self.assertEqual(response.status_code, 200)

    def test_learner_dashboard(self):
        self.client.login(username='learner', password='password')
        response = self.client.get(reverse('dashboard_learner'))
        self.assertEqual(response.status_code, 200)

