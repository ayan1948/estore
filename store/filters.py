import django_filters
from .models import Laptop, Smartphone, filters


class LaptopsFilters(django_filters.FilterSet):
    brand = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Brand'])
    price = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Price'])
    screen = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Screen Size'])
    processor = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Processor'])
    ram = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['RAM'])
    storage = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Storage'])
    OS = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Operating System'])
    graphics = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Graphics'])
    color = django_filters.MultipleChoiceFilter(choices=filters['Laptop.json']['Color'])
    fingerprint = django_filters.BooleanFilter()
    touchscreen = django_filters.BooleanFilter()

    class Meta:
        model = Laptop
        fields = ['brand', 'processor', 'ram', 'storage', 'OS', 'graphics', 'color', 'screen', 'price', 'fingerprint', 'touchscreen']


class SmartphoneFilter(django_filters.FilterSet):
    brand = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Brand'])
    price = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Price'])
    screen = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Screen Size'])
    processor = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Processor'])
    ram = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['RAM'])
    storage = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Storage'])
    OS = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Operating System'])
    color = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Color'])
    frontcamera = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Front Camera'])
    backcamera = django_filters.MultipleChoiceFilter(choices=filters['Smartphone.json']['Back Camera'])

    class Meta:
        model = Smartphone
        fields = ['brand', 'processor', 'ram', 'storage', 'OS', 'color', 'screen', 'price', 'frontcamera', 'backcamera']
