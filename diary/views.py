from django.shortcuts import render

# Create your views here.
from .models import Post
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class PostCreateView(LoginRequiredMixin, CreateView):
  login_url = '/admin/login/'
  model = Post
  fields = ['title', 'body']


# ログイン時、そのユーザーの投稿として保存する

# フォームにCSSをあてる

# 成功した際の遷移先を決める
