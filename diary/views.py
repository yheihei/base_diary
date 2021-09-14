from django.shortcuts import render
from django.views.generic.detail import DetailView

# Create your views here.
from .models import Post
from django.urls import reverse

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class PostDetailView(DetailView):
  model = Post
  # テンプレートの名前を指定する
  template_name = 'diary/post_detail.html'  # 未指定の場合 アプリ名/post_detail.html
  # 取得するクエリを指定
  queryset = Post.objects.select_related(
    'user',  # あらかじめuserテーブルをjoinしておく
  ).prefetch_related(
    'categories',  # あらかじめcategoryテーブルをjoinしておく
  )
  # objectの名前を変更する
  context_object_name = 'post'  # 指定しない場合 object という名前でcontextに渡される

  def get_context_data(self, **kwargs):
    '''
    contextを編集する
    '''
    # contextの取得
    context = super().get_context_data(**kwargs)
    # 編集ページのURLを追加
    if self.request.user.is_authenticated and context[self.context_object_name]:
      post = context[self.context_object_name]
      post.edit_url = reverse(f'admin:{post._meta.app_label}_{post._meta.model_name}_change', args=[post.id] )
    return context

