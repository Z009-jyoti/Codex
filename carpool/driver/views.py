from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rider.models import ride
from django.core import serializers

import numpy as np
import googlemaps
import json

# Assuming you have models defined for Driver and ride, import them here

def driverHome(request):
    print(request.user.username)
    # Assuming Driver is related to User
    driver = Driver.objects.get(user=request.user)
    return render(request, "driverHome.html", {
        'username': request.user.username,
        'vehicle_number': driver.vehicle_number,
    })

def driverInfo(request):
    print(request.user.username + " driveInfo")
    print(request.POST['destination'])
    driver = Driver.objects.get(user=request.user)  # Assuming Driver model is related to User model
    return render(request, "driverProcess1.html", {
        'username': request.user.username,
        'dest': request.POST['destination'],
        'vehicle_number': driver.vehicle_number,
    })

def searchRider(request):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@*******************&&&&&&&&&&&&&&&&&&&&&&&&&&&**********************")
    print(request)
    driverId = request.GET['id']
    liveLat = request.GET['liveLat']
    liveLong = request.GET['liveLong']
    driver_dest = request.GET['destination']
    print(liveLat + "++++++" + liveLong)
    print(request.GET['destination'])
    print("*******************&&&&&&&&&&&&&&&&&&&&&&&&&&&**********************")

    driver = Driver.objects.get(user__username=driverId)  # Get the driver by their username
    vehicle_number = driver.vehicle_number  # Get the vehicle number

    if liveLat == "" or liveLong == "":
        return JsonResponse({'success': False})

    riderSet = ride.objects.select_for_update().filter(status=False, complete=False)
    rideList = []
    print(riderSet)
    print("####################----------------------------------------------------------------------------------------")
    gmaps = googlemaps.Client(key='Your_API_Key')  # Replace with your actual API key
    print("@@@@@@@@@@@@@@@@@@@@@----------------------------------------------------------------------------------------")
    driverRoutePoints = gmaps.directions((float(liveLat), float(liveLong)), driver_dest, mode="driving")

    temp = []
    for leg in driverRoutePoints[0]['legs']:
        for step in leg['steps']:
            html_instructions = step['html_instructions']
            instr = step['distance']['text']
            instrtime = step['duration']['text']
            temp.append(step.get("start_location"))
            temp.append(step.get("end_location"))

    idx = np.round(np.linspace(0, len(temp) - 1, min(10, len(temp)))).astype(int)
    driverRoutePoints = []
    for x in idx:
        driverRoutePoints.append(temp[x])

    print(len(driverRoutePoints), "%%%%%%%%%%%%%%%%%")
    for r in riderSet:
        for point in driverRoutePoints:
            my_dist = gmaps.distance_matrix(point, r.pickUp)['rows'][0]['elements'][0]["distance"]["value"]
            my_dist = my_dist / 1000.0
            expTime = gmaps.distance_matrix(r.pickUp, (liveLat, liveLong))['rows'][0]['elements'][0]["duration"]["text"]
            if my_dist < 60:
                flag = False
                for point in driverRoutePoints:
                    my_dist = gmaps.distance_matrix(point, r.destination)['rows'][0]['elements'][0]["distance"]["value"]
                    my_dist = my_dist / 1000.0
                    if my_dist < 60:
                        flag = True
                        break
                if flag:
                    r.expectedTime = expTime
                    data_dict = {'riderId': r.userId, 'pickUp': r.pickUp, 'destination': r.destination, 'vehicle_number': vehicle_number}
                    rideList.append(data_dict)
                    r.save()
                    break

    return JsonResponse({'rideList': rideList})

def acceptRider(request):
    print(request)
    print("***************************")
    idList = request.GET['id']
    ind = idList.find("&&&----&&&")
    driverId = idList[:ind]
    riderId = idList[ind+10:]
    print(driverId)
    print(riderId)
    
    driver = Driver.objects.get(user__username=driverId)
    vehicle_number = driver.vehicle_number
    success = ride.acceptRide(riderId, driverId)
    acceptedSet = ride.objects.select_for_update().filter(status=True, driverId=driverId, complete=False)
    acceptList = []

    for r in acceptedSet:
        print(r)
        data_dict = {'riderId': r.userId, 'pickUp': r.pickUp, 'destination': r.destination, 'vehicle_number': vehicle_number}
        acceptList.append(data_dict)

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(acceptList)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    return JsonResponse({'success': success, 'acceptList': acceptList})

def endRide(request):
    idList = request.GET['id']
    ind = idList.find("&&&----&&&")
    driverId = idList[:ind]
    riderId = idList[ind+10:]
    print(driverId)
    print(riderId)
    
    driver = Driver.objects.get(user__username=driverId)
    vehicle_number = driver.vehicle_number
    r = get_object_or_404(ride, pk=riderId)
    r.complete = True
    r.save()

    acceptedSet = ride.objects.select_for_update().filter(status=True, driverId=driverId, complete=False)
    acceptList = []

    for r in acceptedSet:
        print(r)
        data_dict = {'riderId': r.userId, 'pickUp': r.pickUp, 'destination': r.destination, 'vehicle_number': vehicle_number}
        acceptList.append(data_dict)

    print(acceptList)
    print("------------------------------------------------- "+str(r.cost) + " ----------------------------------------------")
    return JsonResponse({'success': True, 'acceptList': acceptList, 'cost': r.cost})
