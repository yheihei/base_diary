from django.shortcuts import render
from django.views.generic.detail import DetailView

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class PostDetailView(DetailView):
  model = Post
  # 取得するクエリを指定
  queryset = Post.objects.select_related(
    'user',  # あらかじめuserテーブルをjoinしておく
  ).prefetch_related(
    'categories',  # あらかじめcategoryテーブルをjoinしておく
  )
  # objectの名前を変更する
  context_object_name = 'post'  # 指定しない場合 object という名前でcontextに渡される

