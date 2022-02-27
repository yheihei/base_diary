from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "diary"

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
urlpatterns = [
  path("", views.index, name="index"),
  url(r'^api/', include(router.urls)),
  #JWTトークン生成
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
