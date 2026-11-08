
from django.db import models
from django.conf import settings


# Categories of tasks
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Programming / SQL tasks
class Task(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )

    points = models.PositiveIntegerField(default=100)

    # Temporary old field
    is_completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    difficulty__in=["easy", "medium", "hard"]
                ),
                name="task_valid_difficulty"
            )
        ]

    def __str__(self):
        return self.title


# User solutions and attempts
class Submission(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        WRONG_ANSWER = "wrong_answer", "Wrong Answer"
        ERROR = "error", "Error"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    query = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    score = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

        indexes = [
            models.Index(
                fields=["user", "task", "submitted_at"],
                name="submission_user_task_idx"
            )
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[
                        "pending",
                        "accepted",
                        "wrong_answer",
                        "error"
                    ]
                ),
                name="submission_valid_status"
            )
        ]


    def __str__(self):
        return f"{self.user} - {self.task}"


# Datasets for SQL tasks
class Dataset(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="datasets"
    )

    name = models.CharField(max_length=100)
    setup_sql = models.TextField()
    is_sample = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "name"],
                name="unique_task_dataset"
            )
        ]

    def __str__(self):
        return self.name


# Expected test results
class TestCase(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="test_cases"
    )

    expected_result = models.JSONField(default=list)
    order_matters = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=True)

    def __str__(self):
        return f"Test case {self.id}"
