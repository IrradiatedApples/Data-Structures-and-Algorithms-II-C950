# Created by:
# Arthur J Amende
# Student ID: 002180137

from distance import Distance
from package import Package

from enum import Enum, auto

# Completely defines one Route
class Route:
    # Constructor
    # param start:       Starting address
    # param destination: Destination address
    # param distance:    Route distance
    def __init__(self, start="Mars", destination="Veus", distance=1000):
        self.start = start
        self.destination = destination
        self.distance = distance

    # Print all Route paramaters in a set format
    def print(self):
        print("Start:".ljust(49), "Destination:".ljust(49))
        print(self.start.ljust(49,'.'), self.destination.ljust(49,'.'), self.distance)

# TruckStatus Enum:
# hub - Truck is at the HUB awaiting loading
# driving - Trucks driving and deliverying Packages
class TruckStatus(Enum):
    hub = auto()
    driving = auto()

# Completely defines one Truck
class Truck:
    # Constructor
    # param packages:     Packages loaded onto Truck
    # param distanceHash: Distance Hash Map
    def __init__(self, packages, distanceHash):
        self.loaded_packages = packages
        self.route_travelled = 0
        self.total_travelled = 0
        self.current_route = Route("HUB","HUB",0)
        self.current_packages = []
        self.nextRoute(distanceHash)
        self.status = TruckStatus.driving

    # Loads new Packges onto Truck
    # param packages:     Packages loaded onto Truck
    # param distanceHash: Distance Hash Map
    def load(self, packages, distanceHash):
        self.loaded_packages = packages
        self.current_route = Route("HUB","HUB",0)
        self.current_packages = []
        self.nextRoute(distanceHash)
        self.status = TruckStatus.driving

    # Increments Truck allong current route
    # param dt:    time increment
    # param speed: speed of Truck
    # return: Packages delivered if at destination, otherwise None
    def drive(self, dt, speed):
        self.route_travelled += dt * speed
        self.total_travelled += dt * speed
        # Check if at Destination
        if self.route_travelled >= self.current_route.distance:
            self.route_travelled = 0
            return self.current_packages
        return None

    # Determines the next route using a 'Nearest Neighbor algorithm'
    # param distanceHash: Distance Hash Map
    def nextRoute(self, distanceHash):
        currentAddress = self.current_route.destination
        self.current_route = Route()
        self.current_packages = []

        # All packages delivered, return to HUB
        if not self.loaded_packages:
            distance = distanceHash.search(currentAddress, "HUB").distance
            self.current_route = Route(currentAddress, "HUB", distance)
            # self.current_route.print()
            return

        # Finds the next closest delivery address and sets route
        for package in self.loaded_packages:
            distance = distanceHash.search(currentAddress, package.getAddress()).distance
            if distance < self.current_route.distance:
                self.current_route = Route(currentAddress, package.getAddress(),distance)
                self.current_packages = [package]
            elif package.address == self.current_packages[0].address:
                self.current_packages.append(package)
        self.loaded_packages = [e for e in self.loaded_packages if e not in self.current_packages]
        # self.current_route.print()

    # Print Packages on Truck
    def printPacakges(self):
        for package in self.loaded_packages:
            package.print()
        print()