# Generated by Django 4.2 on 2024-04-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
