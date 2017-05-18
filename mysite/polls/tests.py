from django.test import TestCase
from django.urls import reverse

from django.utils import timezone
import datetime

from .models import Question

# Create your tests here.


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() should return False for
        questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions
        whose pub_date was within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionViewTests(TestCase):

    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should display on the index page.
        """
        create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ['<Question: Past Question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a future pub_date should not display.
        """
        # create_question("Past question.", -30)
        create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_veiw_with_future_question_and_past_question(self):
        """
        Even if past and future questions exist,
        only past questions should display.
        """
        create_question("Past question.", -30)
        create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ['<Question: Past question.>']
        )

    def test_index_view_with_past_questions(self):
        """
        The questions page may display multiple questions.
        """
        create_question(question_text="Q1", days=-30)
        create_question(question_text="Q2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ['<Question: Q2>',
             '<Question: Q1>', ]
        )


class QuestionIndexDetailTests(TestCase):

    def test_detail_view_with_future_Question(self):
        """
        The detail view of a question with a future pub_date
        should return 404
        """
        future_question = create_question(
            question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a past pub_date
        should return the question's text.
        """
        past_question = create_question(question_text="Past.", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
