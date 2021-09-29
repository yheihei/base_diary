from django.shortcuts import render

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


class PostUpdateView(UpdateView):
  # template_name = 'diary/post_form.html'  # デフォルトはアプリ名/モデル名_form.html
  model = Post
  fields = ['title', 'body', 'categories']
  success_url = reverse_lazy('diary:index')

  def form_valid(self, form: Post):
    object: Post = form.save(commit=False)
    object.updated_by = self.request.user
    object.save()
    return super().form_valid(form)
