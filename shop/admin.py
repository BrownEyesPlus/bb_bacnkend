from django.contrib import admin
from .models import Type, Blog, Category, User

# Register your models here.

admin.site.register(Type)
admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Category)
