from django.db.models import fields
from diary.models import Post, Category, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ('name', 'slug')


class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  categories = CategorySerializer(many=True, read_only=True)

  class Meta:
    model = Post
    fields = ('id', 'user', 'title', 'body', 'created_at', 'updated_at', 'categories')
