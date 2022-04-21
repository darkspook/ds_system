from django.contrib import admin
from .models import Asset, Component, EndUser, Brand, Location, Type

admin.site.register(Asset)
admin.site.register(Component)
admin.site.register(EndUser)
admin.site.register(Brand)
admin.site.register(Location)
admin.site.register(Type)