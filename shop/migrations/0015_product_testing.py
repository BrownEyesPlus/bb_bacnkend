# Generated by Django 4.1.3 on 2022-11-30 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='testing',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
