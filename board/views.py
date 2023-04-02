from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from board.forms import TaskForm, SearchForm, ProjectForm, WorkerCreationForm
from board.models import Task, Project, Worker


class IndexListView(generic.ListView):
    model = Project
    template_name = "board/index.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_criteria = self.request.GET.get("search_criteria", "")
        context["search_form"] = SearchForm(
            initial={"search_criteria": search_criteria}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["search_criteria"]
            )
        return queryset


class UserProjectListView(generic.ListView):
    model = Project
    template_name = "board/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_criteria = self.request.GET.get("search_criteria", "")
        context["search_form"] = SearchForm(
            initial={"search_criteria": search_criteria}
        )
        return context

    def get_queryset(self):
        user_pk = self.kwargs.get("pk")
        queryset = Project.objects.filter(tasks__assignees=user_pk)
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["search_criteria"]
            )
        return queryset


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("board:index")


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_criteria = self.request.GET.get("search_criteria", "")
        context["search_form"] = SearchForm(
            initial={"search_criteria": search_criteria}
        )
        context["task_list"] = kwargs.get("object").tasks
        form = SearchForm(self.request.GET)

        if form.is_valid():
            search_criteria = form.cleaned_data["search_criteria"]
            context["task_list"] = context["task_list"].filter(
                name__icontains=search_criteria
            )

        return context


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("board:index")


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy("board:index")
    template_name = "board/confirm_delete.html"


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy("login")


class UserTaskListView(generic.ListView):
    model = Task
    template_name = "board/task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_criteria = self.request.GET.get("search_criteria", "")
        context["search_form"] = SearchForm(
            initial={"search_criteria": search_criteria}
        )
        return context

    def get_queryset(self):
        user_pk = self.kwargs.get("pk")
        queryset = Task.objects.filter(assignees=user_pk)
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["search_criteria"]
            )
        return queryset


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("board:index")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("board:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "board/confirm_delete.html"
    success_url = reverse_lazy("board:index")


def toggle_assign_to_task(request, pk):
    worker = get_user_model().objects.get(pk=request.user.id)
    if (
            Task.objects.get(pk=pk) in worker.tasks.all()
    ):  # probably could check if car exists
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("board:task-detail", args=[pk]))


def toggle_task_change_is_completed(request, pk):
    task = Task.objects.get(pk=pk)
    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True
    task.save()
    return HttpResponseRedirect(reverse_lazy("board:task-detail", args=[pk]))
