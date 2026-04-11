from django.contrib import admin

# Register your models here.
from .models import Customer,Measurement,Order

admin.site.register(Customer)
admin.site.register(Measurement)
admin.site.register(Order)
