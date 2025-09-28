from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, TrainViewSet, HotelViewSet, ReservationViewSet,RegisterWithTokenView

router = DefaultRouter()
router.register('flights', FlightViewSet)
router.register('trains', TrainViewSet)
router.register('hotels', HotelViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path("api/register/", RegisterWithTokenView.as_view(), name="api-register"),
]
