from django.db import models
from django.shortcuts import render
from rest_framework import viewsets, serializers
from django.db.models import Prefetch
from rest_framework import mixins

from diary.models import Star

# Create your views here.
from .models import Post

# Create your views here.
def index(request):
  posts = Post.objects.all()
  if request.user.is_authenticated:
    posts = posts.prefetch_related(
      Prefetch(
        'star_set',
        queryset=Star.objects.filter(user=request.user),
        to_attr='stars'
      )
    )
  return render(request, 'index.html', {
    'posts': list(posts),
  })


class StarSerializer(serializers.ModelSerializer):
  class Meta:
    model = Star
    fields = ('id', 'post', 'user', 'created_at', 'updated_at',)


class StarViewSet(viewsets.ModelViewSet):
  queryset = Star.objects.all()
  serializer_class = StarSerializer
