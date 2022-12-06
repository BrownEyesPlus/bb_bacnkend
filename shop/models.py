from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html

# Create your models here.


class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MyModelBase(models.Model):
    name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='shop/%Y/%m', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __tr__(self):
        return self.name

    class Meta:
        abstract = True


class User(AbstractUser):
    MEN, WOMEN = range(2)
    GENDER = [
        (MEN, 'man'),
        (WOMEN, 'women')
    ]
    avatar = models.ImageField(upload_to='upload/%Y/%m', null=True)
    phone = models.CharField(max_length=20, null=True)
    gender = models.BooleanField(choices=GENDER, default=MEN,  null=True)
    address1 = models.CharField(max_length=1024, null=True)
    birth_year = models.DateField(null=True)


class Type(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255, null=False)
    discount = models.IntegerField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, null=False)
    color_code = models.CharField(max_length=10, null=False, default='#eee')

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=500, null=False)
    description = models.CharField(max_length=500, null=False, default='')
    image = models.ImageField(upload_to='blogs/%Y/%m', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    gender = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'category')
        ordering = ["-id"]


class BaseProduct(MyModelBase):
    category = models.ForeignKey(
        Category, related_name="base_product", on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(
        Type, related_name="base_product", on_delete=models.SET_NULL, null=True)
    discount = models.ForeignKey(
        Discount, related_name="base_product", on_delete=models.SET_NULL, null=True)
    materials = models.ManyToManyField(
        Material, related_name="materials", blank=True, null=True)
    code_name = models.CharField(max_length=20, null=False, unique=True)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=500, null=False, default='')

    def __str__(self):
        return self.name


class Favorite(TimeStamp):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    base_product = models.ForeignKey(
        BaseProduct, on_delete=models.CASCADE, related_name='favorites_baseproduct')

    class Meta:
        unique_together = ('user', 'base_product')


class Rating(TimeStamp):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings')
    base_product = models.ForeignKey(
        BaseProduct, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(null=False)

    class Meta:
        unique_together = ('user', 'base_product')


class ProductColor(TimeStamp):
    base_product = models.ForeignKey(
        BaseProduct, on_delete=models.CASCADE, related_name="product_colors")
    color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, related_name="product_colors", null=True)
    image = models.ImageField(upload_to='products/%Y/%m', null=True)

    def __str__(self):
        return self.base_product.name + ' - ' + self.color.name

    class Meta:
        unique_together = ('color', 'base_product')


class Product(TimeStamp):
    product_color = models.ForeignKey(
        ProductColor, on_delete=models.CASCADE, related_name="product")
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, related_name="product")
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=True)
    testing = models.CharField(max_length=255, null=True,)

    def __str__(self):
        return self.product_color.base_product.name + ' - ' + self.product_color.color.name + ' - ' + self.size.name

    class Meta:
        unique_together = ('size', 'product_color')


class Input(TimeStamp):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="input", null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (self.created_date.strftime('%Y-%m-%d %H:%M'))


class InputDetail(models.Model):
    input = models.ForeignKey(
        Input, on_delete=models.CASCADE, related_name="input_detail")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="input_detail", null=True)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.input.created_date.strftime('%Y-%m-%d %H:%M') + ' - ' + self.product.product_color.base_product.name + ' - ' + self.product.size.name

    class Meta:
        unique_together = ('input', 'product')


class Order(TimeStamp):
    INIT, WAITING, TRANSPORTING, RECEIVED, CANCEL = range(5)
    STATUS = [
        (INIT, 'init'),
        (WAITING, 'waiting'),
        (TRANSPORTING, 'transporting'),
        (RECEIVED, 'received'),
        (CANCEL, 'cancel')
    ]
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="order", null=True)
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, related_name="order", null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=INIT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_detail")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="order_detail", null=True)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.order.created_date.strftime('%Y-%m-%d %H:%M') + ' - ' + self.product.product_color.base_product.name + ' - ' + self.product.size.name

    class Meta:
        unique_together = ('order', 'product')
