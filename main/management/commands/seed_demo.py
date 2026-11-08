
from django.core.management.base import BaseCommand
from main.models import Course, Task, Dataset, TestCase


class Command(BaseCommand):
    help = "Add demo SQL tasks to SUBAY"

    def handle(self, *args, **options):

        categories = [
            ("SQL Basics", "Basic SQL queries"),
            ("SQL Joins", "Working with multiple tables"),
            ("SQL Aggregation", "COUNT, SUM, AVG, GROUP BY"),
        ]

        for title, description in categories:
            if not Course.objects.filter(title=title).exists():
                Course.objects.create(
                    title=title,
                    description=description
                )

        tasks = [
            {
                "course": "SQL Basics",
                "title": "Select All Employees",
                "description": "Select all rows from employees.",
                "difficulty": "easy",
                "points": 100,
                "dataset": "employees_sample",
                "sql": """
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    salary INTEGER
);
INSERT INTO employees VALUES
(1, 'Ali', 5000),
(2, 'Dana', 6500),
(3, 'Mira', 4700);
""",
                "expected": [
                    {"id": 1, "name": "Ali", "salary": 5000},
                    {"id": 2, "name": "Dana", "salary": 6500},
                    {"id": 3, "name": "Mira", "salary": 4700},
                ],
            },
            {
                "course": "SQL Joins",
                "title": "Employees and Departments",
                "description": (
                    "Use JOIN to show employee name "
                    "and department name."
                ),
                "difficulty": "medium",
                "points": 150,
                "dataset": "departments_sample",
                "sql": """
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    department_id INTEGER REFERENCES departments(id)
);
INSERT INTO departments VALUES (1, 'IT'), (2, 'HR');
INSERT INTO employees VALUES
(1, 'Ali', 1),
(2, 'Dana', 2);
""",
                "expected": [
                    {"name": "Ali", "department": "IT"},
                    {"name": "Dana", "department": "HR"},
                ],
            },
            {
                "course": "SQL Aggregation",
                "title": "Count Employees",
                "description": (
                    "Count all employees using COUNT(*). "
                    "Name the result column total."
                ),
                "difficulty": "easy",
                "points": 100,
                "dataset": "employees_count_sample",
                "sql": """
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);
INSERT INTO employees VALUES
(1, 'Ali'), (2, 'Dana'), (3, 'Mira');
""",
                "expected": [{"total": 3}],
            },
        ]

        for item in tasks:
            course = Course.objects.filter(
                title=item["course"]
            ).first()

            task = Task.objects.filter(
                course=course,
                title=item["title"]
            ).first()

            if task is None:
                task = Task.objects.create(
                    course=course,
                    title=item["title"],
                    description=item["description"],
                    difficulty=item["difficulty"],
                    points=item["points"]
                )

            dataset = Dataset.objects.filter(
                task=task,
                name=item["dataset"]
            ).first()

            if dataset is None:
                dataset = Dataset.objects.create(
                    task=task,
                    name=item["dataset"],
                    setup_sql=item["sql"],
                    is_sample=True
                )

            if not TestCase.objects.filter(
                dataset=dataset
            ).exists():
                TestCase.objects.create(
                    dataset=dataset,
                    expected_result=item["expected"],
                    order_matters=False,
                    is_hidden=False
                )

        self.stdout.write(
            self.style.SUCCESS("Demo data created successfully!")
        )
