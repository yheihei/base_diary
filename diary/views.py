from django.shortcuts import render

# Create your views here.
from .models import Post, User
from rest_framework import viewsets, filters
from .serializers import PostSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'posts': Post.objects.all(),
  })


class CategoryFilter(filters.BaseFilterBackend):
  def filter_queryset(self, request, queryset, view):
    if request.query_params.get('category'):
      return queryset.filter(categories__slug=request.query_params.get('category'))
    return queryset


class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [
    filters.SearchFilter,
    filters.OrderingFilter,
    CategoryFilter,
  ]
  search_fields = ('title', 'body')
  ordering_fields = ('created_at', 'updated_at')

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

"""
トークン取得
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"username":"yhei","password":"password"}' http://127.0.0.1:8000/api-token-auth/

トークン使用
curl -X GET http://127.0.0.1:8000/api/posts/ -H 'Authorization: Token 18c26d59a34efb80ee100d55642aa644b1dc9a52'

curl -X POST http://127.0.0.1:8000/api/posts/ -H "Content-Type: application/json" -H 'Authorization: Token 18c26d59a34efb80ee100d55642aa644b1dc9a52' -d '{"title":"title", "body":"body"}'

curl -X PUT http://127.0.0.1:8000/api/posts/3/ -H "Content-Type: application/json" -H 'Authorization: Token 18c26d59a34efb80ee100d55642aa644b1dc9a52' -d '{"title":"title", "body":"body"}'

curl -X PATCH http://127.0.0.1:8000/api/posts/3/ -H "Content-Type: application/json" -H 'Authorization: Token 18c26d59a34efb80ee100d55642aa644b1dc9a52' -d '{"body":"パッチで更新してみた"}'
"""
