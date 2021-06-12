from django.shortcuts import render
from django.urls import reverse

from diary.models import Post
from diary.forms import PostForm
from django.views.generic import UpdateView


def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })

class PostUpdateView(UpdateView):
  model = Post
  template_name = 'post_update_view.html'
  form_class = PostForm
