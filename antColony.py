# Ant colony algorithm
# Travelling Salesman Problem

### Data is going to be loaded from an external file
### First line will contain amount of cities
### Other lines are going to contain distance to particular cities

### Example file:
### 4 
### 0 1 2 3
### 1 0 4 5
### 2 4 0 6
### 3 5 6 0

from array import *
import random, copy, re, math, time
import subprocess as sp

class Road(object):
    # Init class with road distance, and ID's of the cities connected with this road 
    def __init__(self, distance, city1, city2):
        self.distance = distance
        self.city1_id = city1
        self.city2_id = city2
        self.pheromone = 0    
    
    def showRoadData(self):
        print(f'Distance: {self.distance}')
        print(f'From: {self.city1_id}')
        print(f'To: {self.city2_id}')
        print(f'Pheromone: {self.pheromone}')
    
    def setPheromone(self, pheromone):
        self.pheromone = pheromone
    
    def getDistance(self):
        return self.distance

class Ant(object):
    def __init__(self, start_city, pheromone):
        self.Qpheromone = pheromone
        self.roads = list()
        self.cities = list()
        self.totalDistance = 0
        self.start_city_id = start_city
    
    def showAntDetails(self):
        print(f'Pheromone: {self.Qpheromone}')
        print(f'Begin city: {self.start_city_id}')
        print(f'Total distance: {self.totalDistance}')
        roads_string = ''
        for road in self.roads: 
            roads_string = roads_string + ' -> ' + str(road.getDistance())
        
        print(f'Road: {roads_string}')

    # The ant remembers given road
    # Road object is saved in roads list
    def rememberRoad(self, road):
        self.roads.append(road)
    
    # The ant remembers given city_id 
    # City id is saved in cities list
    def rememberCity(self, city_id):
        self.cities.append(city_id)

    # Checks if this ant already visited this city
    def wentToCity(self, city_id):
        for c in self.cities:
            if c == city_id:
                return True
        return False
        
    # Checks if this ant already visited this road
    def wentToRoad(self, road):
        for r in self.roads:
            if r == road:
                return True
        return False
    
    # return calculated pheromone
    # Amount of pheromone = Qpheromone / totalDistance
    def getPheromone(self):
        pheromone = self.Qpheromone / self.totalDistance
        return pheromone

    def getTotalDistance(self): 
        return self.totalDistance

class Colony(object):
    # alpha - pheromone attraction constant
    # beta - short path attraction constant
    # p - evaporation constant (0,1)
    # Q - every ants pheromone constant
    # ants - list of Ant objects in the colony
    # all_roads = list of all the roads
    def __init__(self, size, iterations, alpha, beta, p, Q):
        self.size = size
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.Q = Q
        self.ants = list()
        self.all_roads = list()
        self.initRoadsFromFile()
        
    def addRoad(self, road):
        self.all_roads.append(road)
    
    def addAnt(self, ant):
        self.ants.append(ant)
    
    def initRoadsFromFile(self):
        f = open("data.txt", "r")
        f1 = f.readlines()

        for row in range(1, len(f1)):
            line = f1[row]
            distances = list()
            #print(repr(line))
            number = ''
            for i in range(len(line)):
                if line[i].isdigit():
                    number = number + str(line[i])
                else:
                    if number.isdigit():
                        x = int(number)
                        distances.append(x)
                        number = ''

            for i in range(len(distances)):
                r = Road(distances[i], row-1, i)
                self.addRoad(r)

    def showRoads(self):
        for road in self.all_roads:
            print(f'Road: {road.getDistance()}')

if __name__ == "__main__":
    road = Road(10, 1, 2)
    a = Ant(1, 5)
    c = Colony(1, 2, 3, 4, 5, 6)
    c.showRoads()
