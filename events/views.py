# views.py
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from .models import Flight, Train, Hotel, Reservation
from .serializers import FlightSerializer, TrainSerializer, HotelSerializer, ReservationSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        try:
            flight_id = request.data.get('flight')
            train_id = request.data.get('train')
            hotel_id = request.data.get('hotel')
            quantity = int(request.data.get('quantity', 1))
        except ValueError:
            return Response({'error': 'quantity باید عدد باشد'}, status=status.HTTP_400_BAD_REQUEST)

        # چک کردن پرواز
        if flight_id:
            try:
                flight = Flight.objects.get(id=flight_id)
            except Flight.DoesNotExist:
                return Response({'error': 'پرواز یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
            reserved = Reservation.objects.filter(flight=flight, status='active').count()
            if reserved + quantity > flight.capacity:
                return Response({'error': 'ظرفیت پرواز کافی نیست'}, status=status.HTTP_400_BAD_REQUEST)

        # چک کردن قطار
        if train_id:
            try:
                train = Train.objects.get(id=train_id)
            except Train.DoesNotExist:
                return Response({'error': 'قطار یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
            reserved = Reservation.objects.filter(train=train, status='active').count()
            if reserved + quantity > train.capacity:
                return Response({'error': 'ظرفیت قطار کافی نیست'}, status=status.HTTP_400_BAD_REQUEST)

        # چک کردن هتل
        if hotel_id:
            try:
                hotel = Hotel.objects.get(id=hotel_id)
            except Hotel.DoesNotExist:
                return Response({'error': 'هتل یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
            reserved = Reservation.objects.filter(hotel=hotel, status='active').count()
            if reserved + quantity > hotel.number_of_rooms:
                return Response({'error': 'ظرفیت هتل کافی نیست'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class RegisterWithTokenView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_serializer().instance
        token, _ = Token.objects.get_or_create(user=user)
        data = response.data
        data["token"] = token.key
        return Response(data, status=status.HTTP_201_CREATED)
