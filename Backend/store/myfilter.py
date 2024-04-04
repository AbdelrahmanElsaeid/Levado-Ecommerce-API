from .models import Product
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    color = filters.CharFilter(field_name='color__name', lookup_expr='exact')

    class Meta:
        model = Product
        fields = {
            "title": ["icontains"],
            "category": ["exact"],
            "brand": ["exact"],
            "rating": ["exact"],
            "price": ["lte", "gte", "range"],
        }
