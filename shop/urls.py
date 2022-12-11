from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("types", views.TypeViewSet, 'type')
router.register("colors", views.ColorViewSet, 'color')
router.register("sizes", views.SizeViewSet, 'size')
router.register("blogs", views.BlogViewSet, 'blog')
router.register('users', views.UserViewSet)
router.register('base_products', views.BaseProductViewSet, 'base_product')
router.register('product_colors', views.ProductColorViewSet, 'product_colors')
router.register('orders', views.OrdersViewSet, 'orders')
router.register('inputs', views.InputViewSet, 'inputs')


urlpatterns = [
    path('', include(router.urls)),
    path('profiles/me', views.OwnerProfileAPIView.as_view(),
         name='token_obtain_pair'),
    # path('product_colors', views.ProductColorViewSet, name='product_colors')
    # path('orders', views.OrdersViewSet.as_view(), name='orders'),
]
