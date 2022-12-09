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


class OrdersViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Order.objects.all()
    pagination_class = BasePagination
    serializer_class = OrdersSerializer
    ordering_fields = ['-id']
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        orders = OrderDetail.objects.all().order_by('-id')

        return orders

    def retrieve(self, request, pk):
        order_detail = OrderDetail.objects.filter(order__id=pk)
        serializer = OrderDetailSerializer(
            instance=order_detail, many=True, context={'request': request}
        )

        print(request)
        return Response(serializer.data)
        # return Response(OrdersSerializer(order_detail, many=True, context={'request': request}).data)

    def create(self, request):
        products = request.data.get('items')
        address1 = request.data.get('address1')
        user = request.user
        if (request.user.is_anonymous):
            newOrder = Order.objects.create(
                address1=address1
            )
        else:
            newOrder = Order.objects.create(
                user=user,
                address1=address1
            )

        print(request.user.is_anonymous)

        for product_param in products:
            # if (product_param['id']):
                product = Product.objects.get(pk=product_param['id'])
                if (product):
                    OrderDetail.objects.create(
                        product=product,
                        quantity=product_param['quantity'],
                        order=newOrder
                    )

        return Response({"success": "OK!"}, status=status.HTTP_200_OK)

    #     action = request.data.get('action')
    #     if action == 'delete':
    #         prod = Mylikes.objects.filter(
    #             ebook_id=ebook_id, user=request.user
    #         ).first()
    #         if favorite:
    #             favorite.delete()
    #     elif action == 'add':
    #         Mylikes.objects.get_or_create(ebook_id=ebook_id, user=request.user)

    #     return Response()
