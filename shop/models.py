from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.


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
    avatar = models.ImageField(upload_to='upload/%Y/%m',null=True)
    phone = models.CharField(max_length=20, null=True)
    gender = models.BooleanField(null=True)
    address1 = models.CharField(max_length=1024, null=True)
    birth_year = models.DateField(null=True)


class Type(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255, null=False)
    discount = models.IntegerField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Size(models.Model):
    name = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.title


class Color(models.Model):
    name = models.CharField(max_length=50, null=False)
    color_code = models.CharField(max_length=10, null=False, default='#eee')

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=500, null=False)
    description = models.CharField(max_length=500, null=False, default='')
    image = models.ImageField(upload_to='blogs/%Y/%m', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'category')
        ordering = ["-id"]


# class
