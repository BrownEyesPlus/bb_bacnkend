from rest_framework import viewsets, generics, permissions
from .models import Type, Blog, User
from .serializers import *
from .paginator import BasePagination
from rest_framework.parsers import MultiPartParser, JSONParser

# Create your views here.

class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser,]


class OwnerProfileAPIView(generics.RetrieveUpdateAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user


class TypeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class BlogViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        blogs = Blog.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            blogs = blogs.filter(title__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            blogs = blogs.filter(category_id=cate_id)

        return blogs


class BaseProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Type.objects.all()
    pagination_class = BasePagination
    serializer_class = BaseProductSerializer

    def get_queryset(self):
        base_products = BaseProduct.objects.filter(active=True)

        return base_products
