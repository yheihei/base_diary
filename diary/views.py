from django.shortcuts import render

# Create your views here.
from .models import Post
from rest_framework import generics
from .serializers import PostSerializer

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })

class PostList(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
