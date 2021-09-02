from django.shortcuts import render
from django.views.generic import ListView
from diary.models import Post
from django.urls import reverse, reverse_lazy
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

  # ページネーション
  paginate_by = 2
  page_kwarg = 'page'  # 未指定でも良い。デフォルトは'page'

  pagenate_root_url = reverse_lazy('diary:index')

  def get_context_data(self, **kwargs):
    '''
    コンテキストを追加する

    Notes
    -----
    https://docs.djangoproject.com/ja/3.2/topics/class-based-views/generic-display/#adding-extra-context
    '''
    context = super().get_context_data(**kwargs)
    # ログインしていたら、postに編集用のURLを付与する
    if self.request.user.is_authenticated:
      posts = context['posts']
      for post in posts:
        post.edit_url = reverse(f'admin:{post._meta.app_label}_{post._meta.model_name}_change', args=[post.id] )
      context['posts'] = posts
    
    # 検索条件やper_pageを含んだページネーション用URL
    self.pagenate_root_url += '?'
    query_dict = self.request.GET.copy()
    query_dict.pop(self.page_kwarg)  # ページ番号だけは除く
    for key, value in query_dict.items():
      self.pagenate_root_url += f'&{key}={value}'
    context['pagenate_root_url'] = self.pagenate_root_url
    return context

  def get_queryset(self, **kwargs):
    '''
    動的なフィルタリング

    Notes
    -----
    https://docs.djangoproject.com/ja/3.2/topics/class-based-views/generic-display/#dynamic-filtering
    '''
    queryset = super().get_queryset(**kwargs)
    if self.request.GET.get('category'):
      queryset = queryset.filter(
        categories__slug=self.request.GET.get('category')
      )
    return queryset

  def get_paginate_by(self, queryset):
    '''
    per_pageをクエリによって動的に変える

    Notes
    -----
    https://github.com/django/django/blob/stable/3.2.x/django/views/generic/list.py
    '''
    if self.request.GET.get('per_page'):
      self.paginate_by = int(self.request.GET.get('per_page'))
    return super().get_paginate_by(queryset)
