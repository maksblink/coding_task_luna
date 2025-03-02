import django_filters
from .models import Measurement


class MeasurementFilter(django_filters.FilterSet):
    timestamp_after = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    timestamp_before = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
    min_value = django_filters.NumberFilter(field_name="value", lookup_expr="gte")
    max_value = django_filters.NumberFilter(field_name="value", lookup_expr="lte")


    class Meta:
        model = Measurement
        fields = ['sensor', 'timestamp_after', 'timestamp_before', 'min_value', 'max_value']
