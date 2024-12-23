from django.test import TestCase
from courses.models import SCORM, Course
from users.models import CustomUser

class SCORMRuntimeTestCase(TestCase):
    def setUp(self):
        # Create a learner
        self.learner = CustomUser.objects.create_user(username='Care_Learner1', password='password', role='Learner')

        # Create a course and SCORM module
        self.course = Course.objects.create(title="Your Personal Development", description="SCORM Content")
        self.scorm = SCORM.objects.create(
            title="SCORM Module",
            course=self.course,
            launch_url="/course_content/scorm/1/1648213263_your-personal-development-in-care/scormcontent/index.html"
        )

    def test_scorm_runtime_tracking(self):
        self.client.login(username='Care_Learner1', password='password')
        response = self.client.post(f"/courses/scorm/runtime/update/{self.course.id}/", data={
            "progress": 50,
            "status": "in_progress",
            "start_time": "2024-12-23T12:00:00Z",
            "end_time": "2024-12-23T12:30:00Z"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "success")

