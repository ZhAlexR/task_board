from django.shortcuts import render
from django.urls import reverse_lazy
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
    fields = "__all__"
    success_url = reverse_lazy("board:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("board:index")

