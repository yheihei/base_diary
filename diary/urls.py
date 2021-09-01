from django.urls import path
from . import views
from diary.views import PostListView
from django.conf.urls import include, url

app_name = "diary"
urlpatterns = [
  # path("", views.index, name="index"),
  path("", PostListView.as_view(), name="index"),
]
