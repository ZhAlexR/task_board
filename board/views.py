from django.shortcuts import render
from django.views import generic

from board.models import Task


class IndexListView(generic.ListView):
    model = Task
    template_name = "board/index.html"


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskUpdateView(generic.UpdateView):
    model = Task
    