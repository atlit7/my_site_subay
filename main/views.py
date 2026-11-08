from django.shortcuts import render, get_object_or_404
from .models import Course, Task


# Main page: categories and tasks
def home(request):
    courses = Course.objects.prefetch_related(
        "tasks"
    ).order_by("title")

    return render(request, "home.html", {
        "courses": courses
    })


# Detail page for a single task
def task_detail(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related("course"),
        id=task_id
    )

    sample_dataset = task.datasets.filter(
        is_sample=True
    ).first()

    return render(request, "task_detail.html", {
        "task": task,
        "sample_dataset": sample_dataset
    })