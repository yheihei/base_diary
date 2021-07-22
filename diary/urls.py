from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

app_name = "diary"

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
  path("", views.index, name="index"),
  url(r'^api/', include(router.urls)),
  url(r'^api-token-auth/', auth_views.obtain_auth_token),
]
