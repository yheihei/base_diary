from django.db import models
from django.db.models.deletion import CASCADE

from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
  pass

class Post(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=CASCADE)
  title = models.CharField(max_length=2048, verbose_name='タイトル')
  body = models.TextField(verbose_name='本文')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  categories = models.ManyToManyField(
    'Category',
    blank=True,
    related_name="posts",
    verbose_name='カテゴリ',
  )

class Category(models.Model):
  name = models.CharField(max_length=1024)
  slug = models.CharField(max_length=1024)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return f'{self.name}'
