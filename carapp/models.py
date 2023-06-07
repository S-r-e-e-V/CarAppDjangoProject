from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CarType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200)
    car_price = models.DecimalField(max_digits=10, decimal_places=6)
    inventory = models.PositiveIntegerField(default=10)
    instock = models.BooleanField(default=True)

    # description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.car_name


class Buyer(User):
    AREA_CHOICES = [
        ('W', 'Windsor'),
        ('LS', 'LaSalle'),
        ('A', 'Amherstburg'),
        ('L', 'Lakeshore'),
        ('LE', 'Leamington'),
        ('CH', 'Chatham'),
        ('T', 'Toronto')]

    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='CH')
    interested_in = models.ManyToManyField(CarType)
    phone_number = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.first_name


class OrderVehicle(models.Model):
    STATUS_VALUES = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4), ]
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    number_of_Vehicles = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_VALUES, default=0)
    order_date = models.DateField()

    def __str__(self):
        return self.vehicle.car_name

    @staticmethod
    def total_price(self):
        # vehicle = Vehicle.objects.filter(OrderVehicle.vehicle.car_name)
        # price_total = 0
        # for v in vehicle:
        #     price_total = price_total + v.car_price
        # return price_total
        return self.vehicle.car_price * self.number_of_Vehicles
