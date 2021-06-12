from django.urls import path
from . import views

app_name = "diary"
urlpatterns = [
  path("", views.index, name="index"),
  path("<int:pk>/edit", views.PostUpdateView.as_view(), name="update"),
]
