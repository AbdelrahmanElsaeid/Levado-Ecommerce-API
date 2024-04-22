# Generated by Django 4.2 on 2024-04-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_product_price_aed_remove_product_price_egp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_AED',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_EGP',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True),
        ),
        migrations.DeleteModel(
            name='Prices',
        ),
    ]
