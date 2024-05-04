# Generated by Django 4.2 on 2024-04-28 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_vendor_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='description_ar',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='name_ar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='name_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]