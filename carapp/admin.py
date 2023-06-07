from django.contrib import admin
from .models import CarType,Vehicle,Buyer,OrderVehicle

# Register your models here.
admin.site.register(CarType)
admin.site.register(Vehicle)
admin.site.register(Buyer)
admin.site.register(OrderVehicle)