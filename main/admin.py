from django.contrib import admin
from .models import Course, Task, Dataset, TestCase, Submission


admin.site.register(Course)
admin.site.register(Task)
admin.site.register(Dataset)
admin.site.register(TestCase)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "status", "score", "submitted_at")
    readonly_fields = ("user", "task", "query", "status", "score", "submitted_at")

    def has_add_permission(self, request):
        return False