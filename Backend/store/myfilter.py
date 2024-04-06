from .models import Product
from django_filters import rest_framework as filters
import urllib.parse


class ProductFilter(filters.FilterSet):
    color = filters.CharFilter(field_name='color_product__name', lookup_expr='exact')

    class Meta:
        model = Product
        fields = {
            'brand': ['in'],
            "title": ["icontains"],
            "category": ["exact"],
            "brand": ["exact"],
            "rating": ["exact"],
            "price": ["lte", "gte", "range"],
        }

# from django_filters import rest_framework as filters
# from .models import Product
# from django.db.models import Q

# class ProductFilter(filters.FilterSet):
#     color = filters.CharFilter(field_name='color_product__name', lookup_expr='exact')

#     def filter_brand_custom(self, queryset, name, value):
#         brands = value.split(',')  # Split the comma-separated values
#         q_objects = Q()
#         for brand in brands:
#             q_objects |= Q(**{f'{name}__exact': brand.strip()})
#         return queryset.filter(q_objects)

#     class Meta:
#         model = Product
#         fields = {
#             'brand': [],  
#         }
