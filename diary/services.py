from django.http import HttpRequest
from .models import Post
from typing import List, Dict


class IndexViewAppService:
  '''
  トップページに表示するcontextを作成する
  '''

  def __init__(self, request: HttpRequest) -> None:
    self.request = request

  def create_context(self) -> List[Post]:
    posts = Post.objects.all()

    # 件数指定があればlimitをかける
    per_page = self.request.GET.get('per_page')
    if per_page:
      return posts[:int(per_page)]

    return posts
