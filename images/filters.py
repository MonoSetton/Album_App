import django_filters
from django_filters import CharFilter
from django import forms
from .models import Image, Category


class ImageFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Image
        fields = ['name', 'category']


