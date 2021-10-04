from django.shortcuts import render

# Create your views here.
from .models import Post
from .services import TweetGetTimelineService
from django.core.exceptions import PermissionDenied

# Create your views here.
def index(request):
  try:
    timelines = TweetGetTimelineService(user_id=1).get()  # user_idは仮
  except PermissionDenied:
    timelines = []
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
    'timelines': timelines
  })
