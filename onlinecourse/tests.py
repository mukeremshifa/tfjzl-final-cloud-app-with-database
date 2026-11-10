from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Enrollment, Question


class ExamFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='learner',
            password='test-password',
            first_name='Learner',
        )
        self.course = Course.objects.create(
            name='Learning Django',
            description='Django course',
        )
        Enrollment.objects.create(user=self.user, course=self.course)
        question = Question.objects.create(
            course=self.course,
            content='Is Django a Python framework?',
            grade=100,
        )
        self.correct_choice = Choice.objects.create(
            question=question,
            content='Yes',
            is_correct=True,
        )
        Choice.objects.create(
            question=question,
            content='No',
        )

    def test_authenticated_course_page_displays_exam(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('onlinecourse:course_details', args=[self.course.id])
        )

        self.assertContains(response, 'Start Exam')
        self.assertContains(response, 'Is Django a Python framework?')
        self.assertContains(response, 'Yes')

    def test_submission_scores_and_displays_result(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('onlinecourse:submit', args=[self.course.id]),
            {'choice_%s' % self.correct_choice.id: str(self.correct_choice.id)},
        )

        self.assertRedirects(
            response,
            response.url,
        )
        result = self.client.get(response.url)
        self.assertContains(result, 'Congratulations')
        self.assertContains(result, 'score 100/100')
        self.assertContains(result, 'Correct answer: Yes')

# Create your tests here.
