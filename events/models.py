from random import choice
from typing import Any
from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model


class Flight(models.Model):
    flight_number = models.CharField(max_length=10,unique=True)   # مثلا "IR724"
    origin = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    departure_time=models.DateTimeField()
    arrival_time=models.DateTimeField()
    capacity=models.IntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.flight_number} ({self.origin} →{self.destination})"
    
class Train(models.Model):
    train_number=models.CharField(max_length=10,unique=True)
    origin=models.CharField(max_length=50,blank=True, null=True)
    destination=models.CharField(max_length=50,blank=True, null=True)
    departure_time=models.DateTimeField()
    arrival_time=models.DateTimeField()
    capacity=models.IntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.train_number} ({self.origin} →{self.destination})"
    
class Hotel(models.Model):
    hotel_name=models.CharField(max_length=50 ,blank=True ,null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    number_of_rooms=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=20, decimal_places=2)
    def __str__(self):
        return f"{self.hotel_name} ({self.city})"
    
class Reservation(models.Model):
    # ارتباط با User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # این خودش مدل User پروژه رو می‌گیره
        on_delete=models.CASCADE,  # اگر کاربر حذف شد، رزروها هم حذف بشن
        related_name='reservations'  # دسترسی راحت از سمت User
    )
    flight=models.ForeignKey(
            'Flight',
          on_delete=models.SET_NULL,
          blank=True,
          null=True
                             )
    
    
    train=models.ForeignKey(
          'Train',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        
    )
    hotel=models.ForeignKey(
        'Hotel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        CANCELLED = 'cancelled', 'Cancelled'
        PAID = 'paid', 'Paid'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def __str__(self):
        item = self.flight or self.train or self.hotel
        return f"Reservation by {self.user} for {item} ({self.status})"

    
    
    
    



    

