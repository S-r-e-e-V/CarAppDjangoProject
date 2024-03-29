from django.db import models
from django.contrib.auth.models import User, make_password


# Create your models here.
class CarType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    CRUISE_CONTROL = 'Cruise Control'
    AUDIO_INTERFACE = 'Audio Interface'
    AIRBAGS = 'Airbags'
    AIR_CONDITIONING = 'Air Conditioning'
    SEAT_HEATING = 'Seat Heating'
    PARK_ASSIST = 'ParkAssist'
    POWER_STEERING = 'Power Steering'
    REVERSING_CAMERA = 'Reversing Camera'
    AUTO_START_STOP = 'Auto Start/Stop'

    CAR_FEATURES = [
        (CRUISE_CONTROL, 'Cruise Control'),
        (AUDIO_INTERFACE, 'Audio Interface'),
        (AIRBAGS, 'Airbags'),
        (AIR_CONDITIONING, 'Air Conditioning'),
        (SEAT_HEATING, 'Seat Heating'),
        (PARK_ASSIST, 'ParkAssist'),
        (POWER_STEERING, 'Power Steering'),
        (REVERSING_CAMERA, 'Reversing Camera'),
        (AUTO_START_STOP, 'Auto Start/Stop'),
    ]
    car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200)
    car_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField(default=10)
    instock = models.BooleanField(default=True)
    description = models.TextField(max_length=500, blank=True)
    car_features = models.CharField(max_length=100, choices=CAR_FEATURES, blank=True, null=True)

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
        ('T', 'Toronto'),
        ('Wl', "Waterloo")]

    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='CH')
    interested_in = models.ManyToManyField(CarType)
    phone_number = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        # Before saving the instance, hash the password if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class OrderVehicle(models.Model):
    STATUS_VALUES = [
        (0, "cancelled"),
        (1, "placed"),
        (2, "shipped"),
        (3, "delivered"),
    ]
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


class Description(models.Model):
    title = models.CharField(max_length=100)
    project = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LabGroupMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    semester = models.IntegerField()
    url = models.URLField()

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
