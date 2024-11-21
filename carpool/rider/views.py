from django.shortcuts import render  
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ride
import googlemaps
import json
from django.http import JsonResponse

# Create your views here.

def index(request):
    print(request.user.username)
    return render(request, "riderHome.html", {'username': request.user.username})

def rideInfo(request):
    if request.method == "POST":
        print(request.POST['userId'])
        print(request.POST['pickup'])
        print(request.POST['destination'])
        print(request.POST['latVal'])
        print(request.POST['lngVal']) 
        print(type(request.POST))
        
        r = ride(
            userId=request.POST['userId'],
            pickUp=request.POST['pickup'],
            destination=request.POST['destination']
        )
        r.save()
        context = {
            'paramDict': {
                'userId': request.POST['userId'],
                'pickup': request.POST['pickup'],
                'latVal': request.POST['latVal'],
                'lngVal': request.POST['lngVal'],
                'destination': request.POST['destination']
            }
        }
    return render(request, "blank.html", context)

def statusUpdate(request):
    print("here ----------------------------------")
    id = request.GET['id']
    update = request.GET['update']
    gmaps = googlemaps.Client(key='AIzaSyDH5wMptvEAW9Qrgg-Ttxe2r6eSXFsP1pY')  # Replace with your actual API key
    rideDetils = get_object_or_404(ride, pk=id)
    
    # Make the API call and print the response for debugging
    try:
        response = gmaps.distance_matrix(rideDetils.pickUp, rideDetils.destination)
        print("Google Maps API Response:", response)

        # Extract distance
        distance_value = response['rows'][0]['elements'][0].get("distance", {}).get("value", None)
        
        if distance_value is None:
            raise ValueError("Distance value is missing from the response")
        
        my_dist_1 = distance_value / 1000.0  # Convert to kilometers
        my_dist_1 = int(my_dist_1 * 10)  # Adjust as per your logic
        
    except (KeyError, ValueError) as e:
        print("Error:", e)
        return JsonResponse({'success': False, 'error': str(e)})

    print("hello ----------------------------------", id)
    if rideDetils.status:
        if rideDetils.complete:
            return JsonResponse({'success': True, 'driverId': rideDetils.driverId, 'complete': True, 'cost': my_dist_1, 'expectedTime': rideDetils.expectedTime})
        else:
            return JsonResponse({'success': True, 'driverId': rideDetils.driverId, 'complete': False, 'cost': my_dist_1, 'expectedTime': rideDetils.expectedTime})

    return JsonResponse({'success': False, 'driverId': "none", 'complete': False, 'cost': 0, 'expectedTime': rideDetils.expectedTime})

# Uncomment - if we redirect to new page after ride acceptance
def rideSuccessful(request):
    print("kkk ----------------------------------")
    if request.method == "POST":
        id = request.POST['userId']
        print("rider id", id)
        rideDetails = get_object_or_404(ride, pk=id)
    # return render(request, 'polls/results.html', {'rideDetails': rideDetails})
    return HttpResponse("<h1>SUCCESS </h1>")

# def endRide(request):
#     print(request.GET['id'], "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
#     ride.objects.filter(pk=request.GET['id']).delete()
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
#     return render(request, "drive_or_ride.html", {'user': request.GET['id']})

