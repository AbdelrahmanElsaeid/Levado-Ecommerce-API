# Generated by Django 4.2 on 2024-04-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_category_title_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title_en',
            field=models.CharField(max_length=100),
        ),
    ]
