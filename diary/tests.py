from django.test import TestCase
from django.core.management import call_command
import freezegun

from diary.models import Post


# Create your tests here.
class 新着タグ付与バッチ(TestCase):
  '''#4 バッチを自動テストする'''

  # テスト用データを投入する
  fixtures = ['diary/fixtures/tests/test_update_new_tag.json']

  def setUp(self):
    pass

  def tearDown(self):
    pass

  @freezegun.freeze_time('2021-06-09 13:00')
  def test_1(self):
    '''バッチを実行すると 1週間経過した記事 の新着タグが外れること'''
    call_command('update_new_tag')

    # 新着がついているが1週間経過した記事 を取得
    post = Post.objects.get(pk=1)
    self.assertEqual(0, len(post.tags.all()))

  @freezegun.freeze_time('2021-06-09 13:00')
  def test_2(self):
    '''バッチを実行すると 新着タグなし、1週間未経過記事 に新着タグがつくこと'''
    call_command('update_new_tag')

    # 新着がついているが1週間経過した記事 を取得
    post = Post.objects.get(pk=2)
    self.assertEqual(1, len(post.tags.all()))
    self.assertEqual('new', post.tags.first().slug)
