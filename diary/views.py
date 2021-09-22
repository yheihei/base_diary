from django.shortcuts import render

# Create your views here.
from .models import Post
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django import forms

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'body', 'categories']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

  def clean_title(self):
    '''
    特殊なバリデーション
    '''
    title = self.cleaned_data['title']
    if 'ばか' in title:
      raise forms.ValidationError('誹謗中傷ワードはタイトルに設定できません')
    return title


class PostCreateView(LoginRequiredMixin, CreateView):
  '''
  [x] ログイン必須にする
  [x] ユーザーを投稿者として保存できるようにする
  [x] カテゴリーを選べるようにする
  [x] 保存が完了したら特定のページに遷移する
  [x] 特殊なバリデーションを付与する
  [x] フォームにCSSをあてる
  [ ] エラー時のフォームにCSSをあてる
  '''
  login_url = reverse_lazy('admin:login')
  model = Post
  # fields = ['user', 'title', 'body', 'categories']
  form_class = PostForm
  # 保存したら一覧に遷移するようにする
  success_url = reverse_lazy('diary:index')

  def form_valid(self, form):
    '''
    save時に特殊な操作をする
    '''
    # ユーザーを投稿者として保存できるようにする
    object = form.save(commit=False)
    object.user = self.request.user
    object.save()
    return super().form_valid(form)
