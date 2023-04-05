from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from board.models import Project, Task


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline < timezone.now():
            raise forms.ValidationError("Deadline must be in the future.")
        return deadline


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline < timezone.now():
            raise forms.ValidationError("Deadline must be in the future.")
        return deadline


class SearchForm(forms.Form):
    search_criteria = forms.CharField(
        max_length=63,
        label="",
        show_hidden_initial="Search...",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        required=False,
    )


class FilterForm(forms.Form):
    DEADLINE_SORTING = [
        ("deadline", "ascending"),
        ("-deadline", "descending")
    ]

    status = forms.MultipleChoiceField(
        choices=Project.PROJECT_STATUS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    deadline = forms.ChoiceField(
        choices=DEADLINE_SORTING,
        widget=forms.RadioSelect,
    )
