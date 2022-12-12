from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BlogSerializer(ModelSerializer):
    image = SerializerMethodField()
    # category = CategorySerializer()

    def get_image(self, blog):
        request = self.context['request']
        name = blog.image.name
        if name.startswith("statics/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Blog
        fields = ["id", "title", "description", "image",
                  "content", "created_date", "category"]
        depth = 2


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'username', 'password', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = User()
        user = User(**validated_data)
        # user.first_name = validated_data['first_name']
        user.set_password(validated_data['password'])
        user.save()

        return user


class ProductSerializer(ModelSerializer):
    # image2 = SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        # depth = 2

    # def get_image2(self, base_product):
    #     request = self.context['request']
    #     name = base_product.image.name
    #     if name.startswith("statics/"):
    #         path = '/%s' % name
    #     else:
    #         path = '/static/%s' % name

    #     return request.build_absolute_uri(path)


class ProductColorSerializer(ModelSerializer):
    image = SerializerMethodField()
    product = ProductSerializer

    class Meta:
        model = ProductColor
        fields = ["id", "image", "color", "product"]
        depth = 1

    def get_image(self, base_product):
        request = self.context['request']
        name = base_product.image.name
        if name.startswith("statics/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)


class BaseProductSerializer(ModelSerializer):
    image = SerializerMethodField()
    product_colors = ProductColorSerializer

    class Meta:
        model = BaseProduct
        fields = [
            "id",
            "image",
            "name",
            "code_name",
            "description",
            # "category",
            "discount",
            "materials",
            "product_colors",
            "price",
        ]
        depth = 2

    def get_image(self, base_product):
        request = self.context['request']
        name = base_product.image.name
        if name.startswith("statics/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = "__all__"
        depth = 2


class OrdersSerializer(ModelSerializer):
    total_price = SerializerMethodField()
    client = SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        # depth = 1

    def get_total_price(self, obj):
        # result = list()

        # for item in obj.items:
        #     new_item = dict()
        #     new_item['quantity'] = item['quantity']
        #     # new_item['variant_id'] = item['variant_id']
        #     new_item['product'] = ProductSerializer(
        #         Product.objects.get(pk=item['item_id'])
        #     ).data

        #     result.append(new_item)

        total_price = 0
        detail_orders = OrderDetail.objects.filter(order__id=obj.id)
        for detail in detail_orders:
            product = Product.objects.get(pk=detail.product.id)
            total_price += detail.quantity * product.product_color.base_product.price

        return total_price

    def get_client(self, obj):
        user = User.objects.get(pk=2)

        return UserSerializer(user).data

class InputDetailSerializer(ModelSerializer):
    class Meta:
        model = InputDetail
        fields = "__all__"
        depth = 2


class InputSerializer(ModelSerializer):
    # total_price = SerializerMethodField()
    # client = SerializerMethodField()

    class Meta:
        model = Input
        fields = "__all__"
        # depth = 1

    # def get_total_price(self, obj):

    #     total_price = 0
    #     detail_orders = OrderDetail.objects.filter(order__id=obj.id)
    #     for detail in detail_orders:
    #         product = Product.objects.get(pk=detail.product.id)
    #         total_price += detail.quantity * product.product_color.base_product.price

    #     return total_price

    # def get_client(self, obj):
    #     user = User.objects.get(pk=2)

    #     return UserSerializer(user).data
