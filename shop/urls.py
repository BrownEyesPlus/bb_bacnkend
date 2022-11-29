from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("types", views.TypeViewSet, 'type')
router.register("blogs", views.BlogViewSet, 'blog')
router.register('users', views.UserViewSet)

urlpatterns = [
  path('', include(router.urls))
]
