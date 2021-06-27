from django.core.management.base import BaseCommand, CommandError
from diary.models import Post, User, Category

import sys

class Command(BaseCommand):
  help = '新しい記事を投稿するコマンド'

  def add_arguments(self, parser):
    parser.add_argument('--title', type=str)
    parser.add_argument('--body', type=str)
    parser.add_argument('--category_slugs', nargs='*', type=str)

  def handle(self, *args, **options):
    try: 
      post = self.__create_post(options)
      self.stdout.write(self.style.SUCCESS('記事の投稿に成功しました id:"%s"' % post.pk))
    except ValueError as e:
      self.stdout.write(self.style.ERROR(e))
      sys.exit(1)
    except User.DoesNotExist as e:
      self.stdout.write(self.style.ERROR(e))
      sys.exit(1)

  def __create_post(self, options):
    if not options.get('title'):
      raise ValueError('titleは必須です')
    if not options.get('body'):
      raise ValueError('bodyは必須です')
    post = Post.objects.create(
      user=User.objects.first(),
      title=options['title'],
      body=options['body'],
    )
    if options.get('category_slugs'):
      post.categories.set(Category.objects.filter(
        slug__in=options.get('category_slugs')
      ))
    return post
