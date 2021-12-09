# Created by:
# Arthur J Amende
# Student ID: 002180137

from distance import DistanceHash, Distance
from package import Package, PackageHash, PackageStatus
from datetime import datetime, timedelta
import csv

from truck import Truck, TruckStatus

# Import Packages
packageHash = PackageHash(41)
with open("Packages.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        id = int(row[0])
        address = row[1]
        city = row[2]
        zip = row[3]
        weight = int(row[4])
        deadline_time = row[5]
        status = PackageStatus.hub

        #Deadline Date Check
        if (deadline_time == "EOD"):
            deadline = datetime.strptime("5:00 PM", '%I:%M %p').time()
        else:
            deadline = datetime.strptime(deadline_time, '%I:%M %p').time()

        newPackage = Package(id, address, city, zip, weight, deadline, status)
        packageHash.insert(newPackage)
# packageHash.print()

#Import Distances
distanceHash = DistanceHash()
with open("Distances.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rowIndex = 0
    addresses = []
    for row in csv_reader:
        # First row, capture all addresses
        if rowIndex == 0:
            addresses = row[1:len(row)]
            rowIndex += 1
            continue

        colIndex = 1
        for data in row[1:len(row)]:
            if data == "":
                break
            address1 = addresses[rowIndex-1]
            address2 = addresses[colIndex-1]
            if address1 != address2:
                newDistance = Distance(address1, address2,float(data))
                distanceHash.insert(newDistance)
            colIndex += 1
        rowIndex += 1
# distanceHash.print()

# Assumptions
total_packages = 40
packages_per_truck = 16
speed = 18.0 #mph
start_time = datetime.now()
start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0) # 8:00 AM
dt = .1 / speed # (20 seconds)

# Initial Conditions
time = start_time
packages_loaded = 0

# Prepare Truck 1 packages and depature time
packages_truck1 = []
for id in [1, 4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 39, 40]:
    package = packageHash.search(id)
    package.status = PackageStatus.truck1
    packages_truck1.append(package)
truck1 = Truck(packages_truck1, distanceHash)
packages_loaded += len(packages_truck1)
truck1_depature_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0) # 8:00 AM

# Prepare Truck 2 packages and depature time
packages_truck2 = []
for id in [3, 5, 6, 11, 12, 17, 18, 24, 25, 26, 28, 31, 32, 36, 37, 38]:
    package = packageHash.search(id)
    package.status = PackageStatus.truck2
    packages_truck2.append(package)
truck2 = Truck(packages_truck2, distanceHash)
packages_loaded += len(packages_truck2)
truck2_depature_time = start_time.replace(hour=9, minute=5, second=0, microsecond=0) # 9:05 AM

# Prompt User for Status View Times
print("Welcome to the WGUPS Package Tracking System!")
print("Please enter the times you want to view the status of all packages.")
print("Format time in 24hr code: 13:30 -> 1:30 PM")
print("Only times after 8:00 AM will be displayed.")
print("Enter no time when complete.")
print("If no times are entered the default times of 9:05 AM, 10:00 AM, and 12:30 AM will be displayed.")
print()
input_time = input("View Status at: ")
user_times = []
while input_time != "":
    try:
        new_time = time.strptime(input_time, '%H:%M')
        new_datetime = datetime.combine(start_time.date(), new_time.time())
        user_times.append(new_datetime)
    except:
        print("Incorrent Format")
        print()
    input_time = input("View Status at: ")
print()

default_times =[start_time.replace(hour=9, minute=5, second=0, microsecond=0), start_time.replace(hour=10, minute=0, second=0, microsecond=0), start_time.replace(hour=12, minute=30, second=0, microsecond=0)]

if user_times:
    status_times = user_times
else:
    status_times = default_times

# Step through time in increments of dt (20 seconds)
packages_delivered = 0
while time <= max(status_times):

    time += timedelta(hours=dt)
    
    # View Status
    if time in status_times:
        print("Time: ", time.time())
        packageHash.print()
        print()
        print("Truck 1 Distance Travelled:", format(truck1.total_travelled,".1f"),end="")
        print("     Truck 2 Distance Travelled:", format(truck2.total_travelled,".1f"),end="")
        print("     Total Distance Travelled:", format(truck1.total_travelled + truck2.total_travelled,".1f"))
        print()

    # Update Package 9 at 10:20 AM
    if time == start_time.replace(hour=10, minute=20, second=0, microsecond=0):
        updatePackage = packageHash.search(9)
        updatePackage.id = 9
        updatePackage.address = "410 S State St"
        updatePackage.city = "Salt Lake City"
        updatePackage.zip = "84111"
    
    # Update Truck 1
    # If Truck 1 reached its destination truck1.drive will return
    # a list of packages delivered then a nextRoute selected.
    # If an empty list is returned Truck 1 has returned to HUB.
    # If there are still packages at the HUB they will be
    # loaded onto Truck 1 for delivery.
    if time >= truck1_depature_time:
        if truck1.status == TruckStatus.driving:
            delivered_packages1 = truck1.drive(dt, speed)
            if delivered_packages1 is not None:
                if delivered_packages1:
                    # print("Package(s) Delivered at:", time.time())
                    for package in delivered_packages1:
                        package.status = PackageStatus.delivered
                        package.delivery_time = time.time()
                        # package.print()
                    # print()
                    packages_delivered += len(delivered_packages1)
                    truck1.nextRoute(distanceHash)
                else:
                    truck1.status = TruckStatus.hub
                    # travel_time = (time - truck1_depature_time).seconds / 3600.0
                    # print("Truck 1 returned to HUB at", time.time())
                    # print("Distance Travelled:", format(truck1.total_travelled,".1f"))
                    # print("Travel Time:", format(travel_time,".2f"), "hours")
                    # print("Avg. Speed:", format(truck1.total_travelled / travel_time,".1f"))
                    # print()
        if truck1.status == TruckStatus.hub and packages_loaded < total_packages:
            packages_truck1 = []
            for id in [2, 9, 10, 22, 23, 27, 33, 35]:
                package = packageHash.search(id)
                package.status = PackageStatus.truck1
                packages_truck1.append(package)
            truck1.load(packages_truck1, distanceHash)
            packages_loaded += len(packages_truck1)
    
    # Update Truck 2
    # If Truck 2 reached its destination truck2.drive will return
    # a list of packages delivered then a nextRoute selected.
    # If an empty list is returned Truck 2 has returned to HUB.
    # If there are still packages at the HUB they will be
    # loaded onto Truck 2 for delivery.
    if time >= truck2_depature_time:
        if truck2.status == TruckStatus.driving:
            delivered_packages2 = truck2.drive(dt, speed)
            if delivered_packages2 is not None:
                if delivered_packages2:
                    # print("Package(s) Delivered at:", time.time())
                    for package in delivered_packages2:
                        package.status = PackageStatus.delivered
                        package.delivery_time = time.time()
                        # package.print()
                    # print()
                    packages_delivered += len(delivered_packages2)
                    truck2.nextRoute(distanceHash)
                else:
                    truck2.status = TruckStatus.hub
                    # travel_time = (time - truck2_depature_time).seconds / 3600.0
                    # print("Truck 2 returned to HUB at", time.time())
                    # print("Distance Travelled:", format(truck2.total_travelled,".1f"))
                    # print("Travel Time:", format(travel_time,".2f"), "hours")
                    # print("Avg. Speed:", format(truck2.total_travelled / travel_time,".1f"))
                    # print()
        if truck2.status == TruckStatus.hub and packages_loaded < total_packages:
            packages_truck2 = []
            for id in [2, 9, 10, 22, 23, 27, 33, 35]:
                package = packageHash.search(id)
                package.status = PackageStatus.truck2
                packages_truck2.append(package)
            truck2.load(packages_truck2, distanceHash)
            packages_loaded += len(packages_truck2)

print("End Program")