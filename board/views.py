from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from board.models import Task, Project


class IndexListView(generic.ListView):
    model = Project
    template_name = "board/index.html"

    def get_queryset(self):
        self.queryset = Project.objects.all()
        user_id = self.kwargs.get("pk")
        if user_id:
            self.queryset = Project.objects.filter(tasks__assignees__id=3)
        return self.queryset


class ProjectDetailView(generic.DetailView):
    model = Project
    queryset = Project.objects.prefetch_related("tasks")
    template_name = "board/project_details.html"

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

