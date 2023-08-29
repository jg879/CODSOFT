from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    rating = models.FloatField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='hotel',null = True,blank = True)
    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='room',null = True,blank = True)
    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_charge = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    check_in_date = models.DateField(blank=True,null=True,default=None)
    check_out_date = models.DateField(blank=True,null=True,default=None)
    def __str__(self):
        return f"{self.room_type} at {self.hotel}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField(blank=True,null=True)
    check_out_date = models.DateField(null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f"Booking for {self.user}"
