# Generated by Django 4.2 on 2024-04-01 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, default='brand.jpg', null=True, upload_to='brand')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'ordering': ['country'], 'verbose_name_plural': 'Taxes'},
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.brand'),
        ),
    ]