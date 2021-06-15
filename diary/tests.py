from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class TestIndexView(TestCase):
  '''#1 画面表示を自動テストする'''

  # テスト用データを投入する
  fixtures = ['diary/fixtures/test/test_index_view.json']

  def setUp(self):
    pass
  
  def test_1(self):
    '''一覧に日記コンテンツが表示されている'''
    c = Client()
    response = c.get(reverse('diary:index'))
    posts = response.context['posts']

    with self.subTest(message="2つ以上記事がある"):
      self.assertGreater(len(posts), 1)

    # 記事にタイトル、本文、カテゴリが存在する
    with self.subTest(message="記事にタイトル、本文、カテゴリが存在する"):
      post = posts[0]
      self.assertEqual('タイトル1', post.title)
      self.assertEqual('<p>一つ目の日記本文', post.body)
      self.assertEqual('diary', post.categories.first().slug)
