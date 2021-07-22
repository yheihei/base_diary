from django.urls import path
from . import views

app_name = "diary"
urlpatterns = [
  path("", views.index, name="index"),
  path("api/posts/", views.PostList.as_view(), name="api-posts"),
]
