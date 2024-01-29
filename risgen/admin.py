from django.contrib import admin

from .models import IssuingRIS, IssuingRISItems

admin.site.register(IssuingRIS)
admin.site.register(IssuingRISItems)