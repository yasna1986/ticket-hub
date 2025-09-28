from django.contrib import admin
from .models import Flight,Hotel,Train,Reservation

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display=("flight_number", "origin", "destination", "departure_time", "arrival_time", "price")
    search_fields=("flight_number", "origin", "destination",)
    list_filter=("origin", "destination")
    
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display=("hotel_name","city","number_of_rooms","price")
    search_fields=("hotel_name","city")
    list_filter=("city",)
    
    
@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display= ("train_number","origin","destination","departure_time","arrival_time","capacity","price")
    search_fields=("train_number","origin","destination")
    list_filter=("origin","destination")
    

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "get_item", "status", "quantity", "reservation_date")
    search_fields = ("user__username", "flight__flight_number", "train__train_number", "hotel__hotel_name")
    list_filter = ("status", "reservation_date")

    def get_item(self, obj):
        """برمی‌گردونه نام پرواز/قطار/هتل برای رزرو"""
        return obj.flight or obj.train or obj.hotel
    get_item.short_description = "Reserved Item"
