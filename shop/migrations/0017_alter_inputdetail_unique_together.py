# Generated by Django 4.1.3 on 2022-12-11 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_remove_product_testing_order_address1'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inputdetail',
            unique_together=set(),
        ),
    ]
