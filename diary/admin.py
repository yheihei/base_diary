from django.contrib import admin
from .models import User, Post, Category, Star

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Star)
