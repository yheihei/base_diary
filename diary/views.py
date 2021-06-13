from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse

from diary.models import Post, Category, PostMeta
from diary.forms import PostForm, PostMetaForm
from django.views.generic import UpdateView


def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })

class PostUpdateView(UpdateView):
  model = Post
  template_name = 'post_update_view.html'
  form_class = PostForm

  def get_success_url(self) -> str:
    return reverse('diary:update', kwargs={'pk': self.kwargs['pk']})

  def get_context_data(self, **kwargs):
    context = super(PostUpdateView, self).get_context_data(**kwargs)

    # post_metaのformを作る
    post = context['post']
    context['post_metas'] = PostMeta.objects.filter(post=post)
    post_meta_forms = []
    for post_meta in context['post_metas']:
      post_meta_forms.append(PostMetaForm(post_meta.__dict__))
    context['post_meta_forms'] = post_meta_forms

    return context
  
  def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
    print(request.POST)
    # print(form)
    # todo https://qiita.com/momomo_rimoto/items/625c188ca4fd917d231c
    return super().post(request, *args, **kwargs)
