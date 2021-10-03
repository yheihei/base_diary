from django.urls import path
from . import views

app_name = "diary"
urlpatterns = [
  path("", views.index, name="index"),
  path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
