from django import forms
from django.utils import timezone

from board.models import Project


class ProjectCreateForm(forms.ModelForm):
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


class SearchForm(forms.Form):
    search_criteria = forms.CharField(
        max_length=63,
        label="",
        show_hidden_initial="Search...",
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
        required=False,
    )

