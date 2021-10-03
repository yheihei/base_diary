from django.shortcuts import render

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class PostDeleteView(LoginRequiredMixin, DeleteView):
  # ログインURLも指定する
  login_url = reverse_lazy('admin:login')
  model = Post
  success_url = reverse_lazy('diary:index')

  # template_name = 'post_confirm_delete.html'  # デフォルトはアプリ名/モデル名_confirm_delete.html
