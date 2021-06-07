from django.shortcuts import render

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })