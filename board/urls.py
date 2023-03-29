from django.urls import path

from board.views import IndexListView

app_name = "board"

urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
]
