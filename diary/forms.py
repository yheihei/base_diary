from django import forms
from diary.models import Post

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('user', 'title', 'body')
