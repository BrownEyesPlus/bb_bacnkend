from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("types", views.TypeViewSet, 'type')
router.register("blogs", views.BlogViewSet, 'blog')
router.register('users', views.UserViewSet)
router.register('base_products', views.BaseProductViewSet, 'base_product')
router.register('product_colors', views.ProductColorViewSet, 'product_colors')


urlpatterns = [
    path('', include(router.urls)),
    path('profiles/me', views.OwnerProfileAPIView.as_view(),
         name='token_obtain_pair'),
    # path('product_colors', views.ProductColorViewSet, name='product_colors')
]
