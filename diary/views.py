from django.shortcuts import render
from django.views.generic import ListView
from diary.models import Post
from django.urls import reverse
from django.db.models import Prefetch

# Create your views here.
from .models import Post

# Create your views here.
# def index(request):
#   return render(request, 'index.html', {
#     'posts': Post.objects.all(),
#   })

class PostListView(ListView):
  model = Post
  # 「親切な」テンプレートコンテキストを作る
  # https://docs.djangoproject.com/ja/3.2/topics/class-based-views/generic-display/#making-friendly-template-contexts
  context_object_name = 'posts'

  # オブジェクトのサブセットを表示する
  # https://docs.djangoproject.com/ja/3.2/topics/class-based-views/generic-display/#viewing-subsets-of-objects
  queryset = Post.objects.order_by(
    '-created_at'  # 作成日の新しいものから並べる
  ).select_related(
    'user',  # あらかじめuserテーブルをjoinしておく
  ).prefetch_related(
    'categories',  # あらかじめcategoryテーブルをjoinしておく
  )

  # コンテキストを追加する
  # https://docs.djangoproject.com/ja/3.2/topics/class-based-views/generic-display/#adding-extra-context
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # ログインしていたら、postに編集用のURLを付与する
    if self.request.user.is_authenticated:
      posts = context['posts']
      for post in posts:
        post.edit_url = reverse(f'admin:{post._meta.app_label}_{post._meta.model_name}_change', args=[post.id] )
      context['posts'] = posts
    return context

  # 動的なフィルタリング
  # https://docs.djangoproject.com/ja/3.2/topics/class-based-views/generic-display/#dynamic-filtering
  def get_queryset(self):
    if self.request.GET.get('category'):
      self.queryset = self.queryset.filter(
        categories__slug=self.request.GET.get('category')
      )
    return self.queryset
