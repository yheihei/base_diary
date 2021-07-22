from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
  pass

class Post(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=CASCADE)
  title = models.CharField(max_length=2048)
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  categories = models.ManyToManyField(
    'Category',
    blank=True,
    related_name="posts",
  )

class Category(models.Model):
  name = models.CharField(max_length=1024)
  slug = models.CharField(max_length=1024)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return f'{self.name}'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)
