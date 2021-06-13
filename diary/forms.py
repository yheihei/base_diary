from django import forms
from diary.models import Post

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('user', 'title', 'body', 'categories')
  
  def __init__(self, *args, **kwargs):
    super(PostForm, self).__init__(*args, **kwargs)
    self.fields['user'].widget.attrs.update({'class' : 'form-control', 'readonly': 'readonly'})
    self.fields['title'].widget.attrs.update({'class' : 'form-control'})
    self.fields['body'].widget.attrs.update({'class' : 'form-control'})
    self.fields['categories'].widget.attrs.update({'class' : 'form-control'})
