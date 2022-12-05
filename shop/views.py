from rest_framework import viewsets, generics, permissions, status
from .models import Type, Blog, User
from rest_framework.decorators import action
from .serializers import *
from .paginator import BasePagination
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

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
    queryset = BaseProduct.objects.all()
    pagination_class = BasePagination
    serializer_class = BaseProductSerializer
    ordering_fields = ['-id']

    def get_queryset(self):
        base_products = BaseProduct.objects.filter(active=True).order_by('-id')

        return base_products

    @action(methods=['get'], detail=True, url_path='product_colors')
    def get_product_colors(self, request, pk):
        base_product = BaseProduct.objects.get(pk=pk)
        # print(base_product)
        product_colors = base_product.product_colors.all()

        return Response(ProductColorSerializer(product_colors, many=True, context={'request': request}).data)


class ProductColorViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = ProductColor.objects.all()
    pagination_class = BasePagination
    serializer_class = ProductColorSerializer
    ordering_fields = ['-id']

    def get_queryset(self):
        product_colors = ProductColor.objects.all().order_by('-id')

        return product_colors


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    pagination_class = BasePagination
    serializer_class = ProductSerializer
    ordering_fields = ['-id']

    def get_queryset(self):
        products = Product.objects.all().order_by('-id')

        return products
