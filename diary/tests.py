from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest

from .services import IndexViewAppService


# Create your tests here.
class TestIndexView(TestCase):
  '''#2 関数を自動テストする'''

  # テスト用データを投入する
  fixtures = ['diary/fixtures/test/test_index_view.json']

  def setUp(self):
    pass
  
  def test_2(self):
    '''件数指定でリクエストを渡すとその件数で記事一覧を返す'''
    request = HttpRequest()
    request.GET['per_page'] = "1"
    posts = IndexViewAppService(request).create_context()

    # 1つ記事が取得されている
    self.assertEqual(len(posts), 1)
