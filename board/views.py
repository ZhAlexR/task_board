from django.shortcuts import render
from django.views import generic

from board.models import Task


class IndexListView(generic.ListView):
    model = Task
    template_name = "board/index.html"
