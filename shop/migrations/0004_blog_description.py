# Generated by Django 4.1.3 on 2022-11-28 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_blog_options_blog_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.CharField(default=models.CharField(max_length=500), max_length=500),
        ),
    ]
