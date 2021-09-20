from django.shortcuts import render

# Create your views here.
from .models import Post
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class PostCreateView(LoginRequiredMixin, CreateView):
  login_url = '/admin/login/'
  model = Post
  fields = ['title', 'body']
  # 保存したら一覧に遷移するようにする(暫定)
  success_url = reverse_lazy('diary:index')

  def form_valid(self, form):
    '''
    投稿の保存処理
    '''
    # ログイン中のユーザーを投稿者として保存する
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(super().get_success_url())

# カテゴリーを選べるようにする

# 特殊なバリデーションを付与する

# フォームにCSSをあてる

# エラー時のフォームにCSSをあてる

# 成功したら詳細画面に遷移するようにする
