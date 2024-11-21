from django.urls import path  # Only import path from django.urls
from . import views
from rider.models import ride

app_name = 'driver'

urlpatterns = [
    path('', views.driverHome, name="driverHome"),
    path('driverInfo', views.driverInfo, name="driverInfo"),
    path('vehicleNum', views.driverInfo, name="vehicleNum"),
    path('driveProcess', views.searchRider, name="searchRider"),
    path('accept', views.acceptRider, name="acceptRider"),
    path('end', views.endRide, name="endRide"),
]

