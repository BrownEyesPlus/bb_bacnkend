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


class ColorViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


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
        orders = Order.objects.all().order_by('-id')

        return orders

    def retrieve(self, request, pk):
        order = Order.objects.get(pk=pk)
        order_detail = OrderDetail.objects.filter(order=pk)
        serializer = OrderDetailSerializer(
            instance=order_detail, many=True, context={'request': request}
        )

        print(order)
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
            if (product_param['id']):
                product = Product.objects.get(pk=product_param['id'])
                # BaseProduct.objects.get(pk=product)
                if (product, product.quantity > 0):
                    OrderDetail.objects.create(
                        product=product,
                        quantity=product_param['quantity'],
                        order=newOrder,
                        # price=product.price
                    )
                    product.quantity -= product_param['quantity']
                    product.save()

        return Response({"success": "OK!"}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='user')
    def get_orders_user(self, request):

        userId = self.request.user.id
        order = Order.objects.filter(user__id=userId).order_by('-created_date')

        return Response((OrdersSerializer(order, many=True, context={'request': request}, ).data))

        # return Response(ProductColorSerializer(product_colors, many=True, context={'request': request}).data)
    #     action = request.data.get('action')
    #     if action == 'delete':
    #         prod = Mylikes.objects.filter(
    #             ebook_id=ebook_id, user=request.user
    #         ).first()
    #         if favorite:
    #             favorite.delete()
    #     elif action == 'add':
    #         Mylikes.objects.get_or_create(ebook_id=ebook_id, user=request.user)


class InputViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Input.objects.all()
    pagination_class = BasePagination
    serializer_class = InputSerializer
    ordering_fields = ['-id']
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        inputs = Input.objects.all().order_by('-id')

        return inputs

    def retrieve(self, request, pk):
        # order = Input.objects.get(pk=pk)
        input_detail = InputDetail.objects.filter(input=pk)
        serializer = InputDetailSerializer(
            instance=input_detail, many=True, context={'request': request}
        )

        # print(order)
        return Response(serializer.data)
    # return Response(OrdersSerializer(order_detail, many=True, context={'request': request}).data)

    def create(self, request):
        products = request.data
        # product_color = request.data.get('product_color')
        # size = request.data.get('size')
        user = request.user
        if (len(request.data) > 0):
            if (request.user.is_anonymous):
                newInput = Input.objects.create()
            else:
                newInput = Input.objects.create(
                    user=user,
                )

            for product_param in products:
                if (product_param['size']):
                    product_color = ProductColor.objects.filter(
                        id=product_param['product_color']).first()
                    size = Size.objects.filter(
                        id=product_param['size']).first()
                    product = Product.objects.filter(
                        size=product_param['size'], product_color=product_param['product_color']).first()
                    print(product)
                    if (product):
                        InputDetail.objects.create(
                            input=newInput,
                            product=product,
                            quantity=product_param['quantity'],
                            price=product_param['price'],
                        )
                        product.quantity += product_param['quantity']
                        product.save()
                    else:
                        newProduct = Product.objects.create(
                            product_color=product_color,
                            size=size,
                            quantity=product_param['quantity']
                        )
                        InputDetail.objects.create(
                            input=newInput,
                            product=newProduct,
                            quantity=product_param['quantity'],
                            price=product_param['price'],
                        )

        print(len(request.data) > 0)

        return Response({"success": "OK!"}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='user')
    def get_orders_user(self, request):

        userId = self.request.user.id
        order = Order.objects.filter(user__id=userId).order_by('-created_date')

        return Response((OrdersSerializer(order, many=True, context={'request': request}, ).data))
