from django.test import TestCase
from courses.models import SCORM, Course

class SCORMPlaybackTestCase(TestCase):
    def setUp(self):
        # Create a test course and SCORM module
        self.course = Course.objects.create(title="Test Course", description="Test Description")
        self.scorm = SCORM.objects.create(
            title="Test SCORM",
            course=self.course,
            launch_url="/course_content/scorm/1/test/index.html"
        )

    def test_scorm_launch_url(self):
        # Verify the SCORM launch URL response
        response = self.client.get(self.scorm.launch_url)
        self.assertEqual(response.status_code, 404)  # Adjust to 200 if the URL is valid and served
