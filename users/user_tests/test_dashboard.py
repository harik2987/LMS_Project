from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser, Branch

class DashboardAccessTestCase(TestCase):
    def setUp(self):
        # Create a branch and assign it to the admin user
        self.branch = Branch.objects.create(name="Admin Branch")
        self.admin = CustomUser.objects.create_user(
            username="admin",
            password="password",
            role="admin",
            branch=self.branch
        )

    def test_admin_dashboard(self):
        self.client.login(username="admin", password="password")
        response = self.client.get(reverse('dashboard_admin'))
        self.assertEqual(response.status_code, 200)
