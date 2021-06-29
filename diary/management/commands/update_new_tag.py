from django.core.management.base import BaseCommand, CommandError
from diary.models import Post, Tag
from django.utils import timezone
import datetime

import sys

class Command(BaseCommand):
  '''新着タグ付与バッチ'''
  help = '投稿時刻が現在時刻から1週間以内の記事に新着タグをつける。1週間経過した記事は新着タグを外す。'

  def add_arguments(self, parser):
    parser.add_argument('--new_tag_slug', type=str)

  def handle(self, *args, **options):
    tag_slug = options.get('new_tag_slug') if options.get('new_tag_slug') else 'new'
    tag = Tag.objects.get(slug=tag_slug)

    now = timezone.now()
    for post in list(Post.objects.all()):
      if post.created_at >= now - datetime.timedelta(weeks=1):
        # 投稿から1週間以内の記事に新着タグをつける
        post.tags.set([tag])
      else:
        # 1週間経過した記事は新着タグを外す
        post.tags.remove(tag)
      post.save()
    self.stdout.write(self.style.SUCCESS('新着タグ付与バッチが正常終了しました'))
