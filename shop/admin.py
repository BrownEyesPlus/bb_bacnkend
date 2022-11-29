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
    list_display = ["thumbnail_preview", "name", "id"]

    # def thumbnail_preview(self, obj):
    #     return obj.thumbnail_preview

    # thumbnail_preview.short_description = 'Thumbnail Preview'
    # thumbnail_preview.allow_tags = True
    def thumbnail_preview(self, product_color):
        return mark_safe('''
        <img width ="auto" height="50" src="/static/{img_url}" />
      '''.format(img_url=product_color.image, alt=product_color.name))


class ProductColorAdmin(admin.ModelAdmin):
    form = ProductColorForm
    search_fields = ["base_product__name", "created_date"]
    list_filter = ["base_product__name"]
    readonly_fields = ["thumbnail"]
    inlines = (BaseProductInline,)

    # class Media:
    #     css = {
    #         'all': ('/static/css/main.css',)
    #     }

    def thumbnail(self, product_color):
        return mark_safe('''
        <img width ="auto" height="50" src="/static/{img_url}" />
      '''.format(img_url=product_color.image, alt=product_color.base_product.name))


admin.site.register(Type)
admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(BaseProduct, BaseProductAdmin)
admin.site.register(Discount)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
