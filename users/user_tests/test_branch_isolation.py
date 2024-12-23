from django.test import TestCase
from users.models import CustomUser, Branch
from courses.models import Course

class BranchIsolationTestCase(TestCase):
    def setUp(self):
        # Create two branches
        self.branch1 = Branch.objects.create(name="Technology")
        self.branch2 = Branch.objects.create(name="Care")

        # Create Admin users for each branch
        self.admin1 = CustomUser.objects.create_user(
            username='admin1', password='password', role='admin', branch=self.branch1
        )
        self.admin2 = CustomUser.objects.create_user(
            username='admin2', password='password', role='admin', branch=self.branch2
        )

        # Create courses for each branch
        self.course1 = Course.objects.create(title="Tech Course", branch=self.branch1)
        self.course2 = Course.objects.create(title="Care Course", branch=self.branch2)

    def test_branch_isolation(self):
        # Admin1: Verify access to branch1 courses only
        self.client.login(username='admin1', password='password')
        response = self.client.get('/users/dashboard/admin/')
        self.assertContains(response, "Tech Course")
        self.assertNotContains(response, "Care Course")

        # Admin2: Verify access to branch2 courses only
        self.client.login(username='admin2', password='password')
        response = self.client.get('/users/dashboard/admin/')
        self.assertContains(response, "Care Course")
        self.assertNotContains(response, "Tech Course")
