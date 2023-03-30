from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from board.forms import ProjectCreateForm
from board.models import Task, Project


class IndexListView(generic.ListView):
    model = Project
    template_name = "board/index.html"

    def get_queryset(self):
        self.queryset = Project.objects.all()
        user_pk = self.request.GET.get("user_pk")
        if user_pk:
            self.queryset = Project.objects.filter(tasks__assignees__id=user_pk)
        return self.queryset


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse_lazy("board:index")


class ProjectDetailView(generic.DetailView):
    model = Project
    queryset = Project.objects.prefetch_related("tasks")


class ProjectUpdateView(generic.UpdateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("board:index")


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy("board:index")
    template_name = "board/confirm_delete.html"


class UserTaskListView(generic.ListView):
    model = Task
    template_name = "board/task_list.html"
    
    def get_queryset(self):
        queryset = super(UserTaskListView, self).get_queryset()
        user_pk = self.kwargs.get("pk")
        return queryset.filter(assignees=user_pk)


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("board:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "board/confirm_delete.html"
    success_url = reverse_lazy("board:index")


def toggle_assign_to_task(request, pk):
    worker = get_user_model().objects.get(id=request.user.id)
    if (
        Task.objects.get(pk=pk) in worker.tasks.all()
    ):  # probably could check if car exists
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("board:task-detail", args=[pk]))
