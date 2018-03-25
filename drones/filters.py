from django_filters.rest_framework import FilterSet
from rest_framework import filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter

from drones.models import Competition


class CompetitionFilter(FilterSet):
    from_achievement_date = DateTimeFilter(name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = DateTimeFilter(name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = NumberFilter(name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = NumberFilter(name='distance_in_feet', lookup_expr='lte')
    drone_name = AllValuesFilter(name='drone__name')
    pilot_name = AllValuesFilter(name='pilot__name')

    class Meta:
        model = Competition
        fields = ('distance_in_feet', 'from_achievement_date', 'to_achievement_date', 'min_distance_in_feet',
                  'max_distance_in_feet',
                  # drone__name will be accessed as drone_name
                  'drone_name',
                  # pilot__name will be accessed as pilot_name
                  'pilot_name',)
