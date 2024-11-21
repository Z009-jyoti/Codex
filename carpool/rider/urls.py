from django.urls import path  # Only import path from django.urls
from . import views

app_name = 'rider'

urlpatterns = [
    path('', views.index, name="ride"),
    path('submit', views.rideInfo, name="rideInfo"),
    path('processsing', views.statusUpdate, name="statusUpdate"),
    path('success', views.rideSuccessful, name="rideSuccessful"),
    # path('rideRemove', views.endRide, name="endRide"),
]

