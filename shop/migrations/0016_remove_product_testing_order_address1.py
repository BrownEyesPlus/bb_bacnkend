# Generated by Django 4.1.3 on 2022-12-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_product_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='testing',
        ),
        migrations.AddField(
            model_name='order',
            name='address1',
            field=models.CharField(default='', max_length=500),
        ),
    ]
