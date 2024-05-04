# Generated by Django 4.2 on 2024-04-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_color_name_ar_color_name_en_product_description_ar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='title_ar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='title_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='title_ar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]