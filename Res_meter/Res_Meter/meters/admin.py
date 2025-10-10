from django.contrib import admin
from .models import Meter, MeterSpecification, MeterReading

admin.site.register(Meter)
admin.site.register(MeterSpecification)
admin.site.register(MeterReading)
