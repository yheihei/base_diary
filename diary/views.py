from django.db import models
from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework import mixins

from diary.models import Star

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  posts = list(Post.objects.all())
  starred_post_ids = {}
  if request.user.is_authenticated:
    stars = Star.objects.filter(
      user=request.user,
      post__in=[post.id for post in posts]
    )
    for star in stars:
      starred_post_ids[star.post.id] = star.id
  return render(request, 'index.html', {
    'posts': posts,
    'starred_post_ids': starred_post_ids,
  })


class StarSerializer(serializers.ModelSerializer):
  class Meta:
    model = Star
    fields = ('id', 'post', 'user', 'created_at', 'updated_at',)


class StarViewSet(viewsets.ModelViewSet):
  queryset = Star.objects.all()
  serializer_class = StarSerializer
