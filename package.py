# Created by:
# Arthur J Amende
# Student ID: 002180137

from enum import Enum, auto
from datetime import datetime

# PackageStatus Enum:
# hub - Package is at the HUB awaiting loading
# truck1 - Package is loaded onto Truck 1
# truck2 - Package is loaded onto Truck 2
# delivered - Package has been delivered to destination
class PackageStatus(Enum):
    hub = auto()
    truck1 = auto()
    truck2 = auto()
    delivered = auto()

# Completely defines one Package
class Package:
    # Constructor
    # param id:       ID number
    # param address:  delivery address
    # param city:     delivery city
    # param zip:      delivery zip code
    # param weight:   package weight (kg)
    # param deadline: delivery deadline time
    # param status:   package status (see PackageStatus Enum)
    def __init__(self, id=0, address="dummy", city="dummy", zip="dummy", weight=0, deadline=datetime.now().time(), status=PackageStatus.hub):
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.weight = weight
        self.deadline = deadline
        self.status = status
        self.delivery_time = None

    # return address + zip code for distance hashmap
    def getAddress(self):
        return self.address + "(" + self.zip + ")"

    # Print all Package paramaters in a set format
    def print(self):
        print(str(self.id).ljust(6),end="")
        print(self.address.ljust(42),end="")
        print(self.city.ljust(20),end="")
        print(self.zip.ljust(12),end="")
        print(str(self.weight).ljust(10),end="")
        print(str(self.deadline.strftime("%I:%M %p")).ljust(12),end="")

        if (self.status == PackageStatus.hub):
            print("At the Hub")
        elif (self.status == PackageStatus.truck1):
            print("En Route - Truck 1")
        elif (self.status == PackageStatus.truck2):
            print("En Route - Truck 2")
        elif (self.status == PackageStatus.delivered):
            print("Delivered at", self.delivery_time)

# Hashing algorithm and table for Packages
class PackageHash:
    # Constructor
    # param modNum: Number of buckets in hash table
    def __init__(self, modNum = 10):
        self.modNum = modNum
        self.table = []
        for i in range(self.modNum):
            self.table.append([])

    # Inserts a Packge into the hash table using
    # Package ID as the 'key'
    # If the Package already exists it is superseded
    # by newPackage
    # parm newPackage: Package to be added to hash table
    def insert(self, newPackage):
        id = newPackage.id
        bucket = id % self.modNum
        bucket_list = self.table[bucket]

        for package in bucket_list:
            if (package.id == id):
                package = newPackage
                return

        bucket_list.append(newPackage)

    # Searches for a Package in the hash table
    # param obj: Package or Package ID to be searched for
    # return: Package if one is found, None if not found
    def search(self, obj):
        if (isinstance(obj, Package)):
            key = obj.id
        else:
            key = obj

        bucket = key % self.modNum
        bucket_list = self.table[bucket]

        for package in bucket_list:
            if (package.id == key):
                return package
        return None

    # Removes a package in the hash table
    # param obj: Package or Package ID to be removed
    def remove(self, obj):
        if (isinstance(obj, Package)):
            key = obj.id
        else:
            key = obj

        bucket = key % self.modNum
        bucket_list = self.table[bucket]

        for package in bucket_list:
            if (package.id == key):
                bucket_list.remove(package)
                return

    # Print packages in a set format
    def print(self):
        print(("ID").ljust(6),end="")
        print(("Address").ljust(42),end="")
        print(("City").ljust(20),end="")
        print(("Zip Code").ljust(12),end="")
        print(("Weight").ljust(10),end="")
        print(("Deadline").ljust(12),end="")
        print(("Status").ljust(14))
        for bucket_list in self.table:
            for package in bucket_list:
                package.print()