from django.shortcuts import render

# Create your views here.
from .models import Post
from django.views.generic.edit import CreateView

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class PostCreateView(CreateView):
  model = Post
  fields = ['title', 'body']


# ログイン必須にする

# ログイン時、そのユーザーの投稿として保存する

# フォームにCSSをあてる

# 成功した際の遷移先を決める
