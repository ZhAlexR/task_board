from django import forms
from django.utils import timezone

from board.models import Project


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "status",
            "deadline",
        )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline < timezone.now():
            raise forms.ValidationError("Deadline must be in the future.")
        return deadline
