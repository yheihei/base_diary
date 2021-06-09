from django.shortcuts import render
from .services import IndexViewAppService

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  posts = IndexViewAppService(request).create_context()
  return render(request, 'index.html', {
    'posts': posts,
  })