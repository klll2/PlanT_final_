import django_filters
from .models import Place, Plan, Trip, Route, Tag,Traveler

class TravelerFilter(django_filters.FilterSet):
    class Meta:
        model = Traveler
        fields = {
            'trvlr_email': ['exact', 'icontains'],
        }

class TripFilter(django_filters.FilterSet):
    class Meta:
        model = Trip
        fields = {
            'trip_traveler': ['exact'],
            'trip_state': ['exact'],
        }
