from django.shortcuts import render

# Create your views here.
from .models import Post
from rest_framework import viewsets, filters
from .serializers import PostSerializer

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
