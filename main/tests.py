from django.test import TestCase
from django.db import IntegrityError, transaction, connection
from django.contrib.auth import get_user_model
from django.core.management import call_command

from main.models import Course, Task, Submission, Dataset


User = get_user_model()


class DatabaseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_student",
            password="TestPassword123!"
        )

        self.course = Course.objects.create(
            title="Test SQL",
            description="Test category"
        )

        self.task = Task.objects.create(
            course=self.course,
            title="Test Task",
            description="Test description",
            difficulty="easy",
            points=100
        )

    # Test 1: Foreign key relationship
    def test_task_course_relationship(self):
        self.assertEqual(self.task.course, self.course)

    # Test 2: CHECK constraint
    def test_invalid_difficulty(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Task.objects.create(
                    course=self.course,
                    title="Wrong Task",
                    description="Invalid difficulty",
                    difficulty="impossible"
                )

    # Test 3: UNIQUE constraint
    def test_duplicate_dataset(self):
        Dataset.objects.create(
            task=self.task,
            name="sample",
            setup_sql="SELECT 1;"
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Dataset.objects.create(
                    task=self.task,
                    name="sample",
                    setup_sql="SELECT 2;"
                )

    # Test 4: User submissions and SQL VIEW
    def test_user_statistics(self):
        Submission.objects.create(
            user=self.user,
            task=self.task,
            query="SELECT 1;",
            status="pending"
        )

        Submission.objects.create(
            user=self.user,
            task=self.task,
            query="SELECT * FROM employees;",
            status="accepted",
            score=100
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT total_attempts,
                       attempted_tasks,
                       solved_tasks
                FROM main_user_statistics
                WHERE user_id = %s
                """,
                [self.user.id]
            )
            result = cursor.fetchone()

        self.assertEqual(result, (2, 1, 1))

    # Test 5: Seed command without duplicates
    def test_seed_demo_no_duplicates(self):
        call_command("seed_demo")

        first_count = Task.objects.count()

        call_command("seed_demo")

        second_count = Task.objects.count()

        self.assertEqual(first_count, second_count)