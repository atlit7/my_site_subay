
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_submission_submission_valid_status_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE VIEW main_user_statistics AS
                SELECT
                    u.id AS user_id,
                    u.username,
                    COUNT(s.id) AS total_attempts,
                    COUNT(DISTINCT s.task_id) AS attempted_tasks,
                    COUNT(DISTINCT s.task_id)
                        FILTER (WHERE s.status = 'accepted')
                        AS solved_tasks
                FROM auth_user u
                LEFT JOIN main_submission s
                    ON u.id = s.user_id
                GROUP BY u.id, u.username;
            """,
            reverse_sql="DROP VIEW IF EXISTS main_user_statistics;"
        ),
    ]
