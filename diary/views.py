from django.shortcuts import render
from django.urls import reverse

from diary.models import Post, Category, PostMeta
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

  def get_context_data(self, **kwargs):
    context = super(PostUpdateView, self).get_context_data(**kwargs)
    post = context['post']
    context['post_metas'] = PostMeta.objects.filter(post=post)
    # TODO post_metasがあったら、これをもとにformを作って contextに含める
    return context
