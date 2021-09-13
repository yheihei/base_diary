from django.urls import path
from . import views
from diary.views import PostDetailView

app_name = "diary"
urlpatterns = [
  path("", views.index, name="index"),
  path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
