from django.contrib import admin
from .models import Place, Route, Trip, Plan, Tag, Traveler

# Register your models here.
admin.site.register(Place)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Traveler)
# admin.site.register(TripTag)