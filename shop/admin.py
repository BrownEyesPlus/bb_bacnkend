from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .models import *

# Register your models here.


class ProductColorForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = ProductColor
        fields = '__all__'


class BaseProductInline(admin.TabularInline):
    model = Product


class BaseProductAdmin(admin.ModelAdmin):
    model = BaseProduct
    readonly_fields = ["thumbnail_preview"]
    search_fields = ["name", "created_date"]
    list_display = ["thumbnail_preview", "name", "id"]

    def thumbnail_preview(self, product_color):
        return mark_safe('''
        <img width ="auto" height="50" src="/static/{img_url}" />
      '''.format(img_url=product_color.image, alt=product_color.name))


class ProductColorAdmin(admin.ModelAdmin):
    # form = ProductColorForm
    model = ProductColor
    search_fields = ["base_product__name", "created_date"]
    list_filter = ["base_product__name", "color"]
    readonly_fields = ["thumbnail"]
    list_display = ["thumbnail", "id", "base_product", "color"]

    # inlines = (BaseProductInline,)

    def thumbnail(self, product_color):
        return mark_safe('''
        <img width ="auto" height="50" src="/static/{img_url}" />
      '''.format(img_url=product_color.image, alt=product_color.base_product.name))


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields = ["product_color__base_product__name", "created_date"]
    list_filter = ["product_color__base_product__name", "product_color__color", "size"]
    readonly_fields = ["thumbnail"]
    list_display = ["thumbnail", "id", "product_color", "size"]

    def thumbnail(self, product):
        return mark_safe('''
        <img width ="auto" height="50" src="/static/{img_url}" />
      '''.format(img_url=product.product_color.image, alt=product.product_color.base_product.name))



class InputDetailAdmin(admin.ModelAdmin):
    model = InputDetail
    # list_filter = ["input"]


admin.site.register(Type)
admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(BaseProduct, BaseProductAdmin)
admin.site.register(Discount)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Material)
admin.site.register(Input)
admin.site.register(InputDetail)
admin.site.register(Order)
admin.site.register(OrderDetail, InputDetailAdmin)
