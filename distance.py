# Created by:
# Arthur J Amende
# Student ID: 002180137

# Stores the distance between two addresses
class Distance:
    # Constructor
    # param address1: First address
    # param address2: Second address
    # param distance: distance between addresses
    def __init__(self, address1="Mars", address2="Venus", distance=1000):
        key1 = hash(address1)
        key2 = hash(address2)

        # Key1 should always be the smallest
        if key2 < key1:
            tempAddress = address1
            address1 = address2
            address2 = tempAddress

        self.address1 = address1
        self.address2 = address2
        self.distance = distance

    # Print all distance paramaters in a set format
    def print(self):
        print(self.address1.ljust(49,'.'), self.address2.ljust(49,'.'), self.distance)

# Hashing algorithm and table for Distances
class DistanceHash:
    # Constructor
    # param modNum: Number of outer and inner buckets in hash table
    def __init__(self, modNum = 10):
        self.modNum = modNum
        self.table = []
        for i in range(self.modNum):
            self.table.append([])
            for j in range(self.modNum):
                self.table[i].append([])

    # Inserts a Distance into the hash table
    # If the Distance already exists it is superseded
    # by newDistance
    # parm newDistance: Distance to be added to hash table
    def insert(self, newDistance):
        key1 = hash(newDistance.address1)
        key2 = hash(newDistance.address2)

        bucket1 = key1 % self.modNum
        outer_bucket_list = self.table[bucket1]

        bucket2 = key2 % self.modNum
        inner_bucket_list = outer_bucket_list[bucket2]

        for distance in inner_bucket_list:
            if (newDistance.address1 == distance.address1 and newDistance.address2 == distance.address2):
                distance = newDistance
                return

        inner_bucket_list.append(newDistance)

    # Searches for a Distance in the hash table
    # param address1: First address
    # param address2: Second address
    # return: Distance if one is found, None if not found
    def search(self, address1, address2):
        if (address1 == address2):
            return Distance(address1, address2, 0)

        key1 = hash(address1)
        key2 = hash(address2)

        key_address1 = address1
        key_address2 = address2
        #Key1 should always be the smallest
        if key2 < key1:
            tempKey = key1
            key1 = key2
            key2 = tempKey
            tempAddress = key_address1
            key_address1 = key_address2
            key_address2 = tempAddress

        bucket1 = key1 % self.modNum
        outer_bucket_list = self.table[bucket1]

        bucket2 = key2 % self.modNum
        inner_bucket_list = outer_bucket_list[bucket2]

        for distance in inner_bucket_list:
            if (distance.address1 == key_address1 and distance.address2 == key_address2):
                return distance

        return None

    # Removes all Distances in the hash table with address
    # param address: address to be removed from hash table
    def remove(self, address):
        key = hash(address)

        bucket = key % self.modNum

        # Check if address is outer key
        outer_bucket_list = self.table[bucket]
        for inner_bucket_list in outer_bucket_list:
            for distance in inner_bucket_list:
                if (distance.address1 == address):
                    inner_bucket_list.remove(distance)
        
        # Check if address is inner key
        for outer_bucket_list in self.table:
            inner_bucket_list = outer_bucket_list[bucket]
            for distance in inner_bucket_list:
                if (distance.address2 == address):
                    inner_bucket_list.remove(distance)

    # Print Distances in a set format
    def print(self):
        print(("Address_1").ljust(49), ("Address_2").ljust(49), "Distance")
        for outer_bucket_list in self.table:
            for inner_bucket_list in outer_bucket_list:
                for distance in inner_bucket_list:
                    distance.print()
        print()