from dataclasses import field
from os import write
from pyexpat import model
from rest_framework import serializers
from .models import Flight, Train, Hotel, Reservation
from django.contrib.auth import get_user_model

class FlightSerializer(serializers.ModelSerializer):
      class Meta:
        model = Flight            # بهش می‌گیم روی مدل Flight ساخته بشه
        fields = '__all__'   
    
class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train         
        fields = '__all__' 
        
class HotelSerializer(serializers.ModelSerializer):
     class Meta:
        model = Hotel         
        fields = '__all__' 
class ReservationSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    train = TrainSerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)

    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), source='flight', write_only=True, required=False
    )
    train_id = serializers.PrimaryKeyRelatedField(
        queryset=Train.objects.all(), source='train', write_only=True, required=False
    )
    hotel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(), source='hotel', write_only=True, required=False
    )

    class Meta:
        model = Reservation
        fields = '__all__'
user=get_user_model
class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True, min_length=6)
    password2=serializers.CharField(write_only=True, min_length=6)
     
    class Meta:
        model=user
        fields=("id","username","email","password","password2")
        extra_kwargs={"email":{"required":False}}
    def validate(self,data):
           if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    def create(self,validated_data):
        password=validated_data.pop("password")
        validated_data.pop("password2", None)
        user = User.objects.create_user(password=password, **validated_data)
        return user