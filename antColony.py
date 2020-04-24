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

    def getPheromone(self):
        return self.pheromone

class Ant(object):
    def __init__(self, start_city, pheromone):
        self.Qpheromone = pheromone
        self.roads = list()
        self.cities = list()
        self.totalDistance = 0
        self.start_city_id = start_city
        self.currentCity = start_city

    def resetTravelData(self):
        self.roads = list()
        self.cities = list()
        self.totalDistance = 0
    
    # Move along the road
    def move(self, road):
        # Remember this city as already visited
        self.cities.append(self.currentCity)
        
        # Add distance of this road to total distance
        addDistance = road.getDistance()
        self.totalDistance = self.totalDistance + addDistance
        
        newCity = road.city1_id
        if newCity == self.currentCity:
            newCity = road.city2_id
        
        # Change the current city
        self.currentCity = newCity

        # Add this road to already used
        self.roads.append(road)
    
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
    
    def getCurrentCity(self):
        return self.currentCity
    
    def setCurrentCity(self, new_city_id):
        self.currentCity = new_city_id

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
        self.cities = 0
        self.ants = list()
        self.all_roads = list()

        self.initRoadsFromFile()
        self.initAnts()
        
    def addRoad(self, road):
        self.all_roads.append(road)
    
    def addAnt(self, ant):
        self.ants.append(ant)
    
    # Reads all the data from file "data.txt" and creates Road objects
    def initRoadsFromFile(self):
        f = open("data.txt", "r")
        f1 = f.readlines()

        # Read amount of cities
        cities_string = ''
        for character in f1[0]:
            if character.isdigit():
                cities_string = cities_string + character
            else:
                self.cities = int(cities_string)

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
                # Don't read roads to the city itself
                if not row-1 == i:
                    r = Road(distances[i], row-1, i)
                    self.addRoad(r)
        
        self.removeRoadDuplicates(0)

    def removeRoadDuplicates(self, begin_index):
        for i in range(begin_index,len(self.all_roads)):
            if i+1 < len(self.all_roads):
                for j in range(i+1, len(self.all_roads)):
                    if self.roadsEqual(self.all_roads[i], self.all_roads[j]):
                        del self.all_roads[j]
                        self.removeRoadDuplicates(i)
                        return
    
    # Check if those 2 roads are the same
    def roadsEqual(self, road1, road2):
        if road1.city1_id == road2.city1_id and road1.city2_id == road2.city2_id:
            return True
        elif road1.city2_id == road2.city1_id and road1.city1_id == road2.city2_id:
            return True
        else:
            return False

    # Init ants by creating objects and giving them a random start location
    def initAnts(self):
        for i in range(self.size):
            start_city_id = random.randrange(self.cities)
            #print(start_city_id)
            a = Ant(start_city_id, self.Q)
            self.ants.append(a)

    # update pheromone value on every road
    def updatePheromoneValue(self):
        for road in self.all_roads:
            deltaPheromone = 0
            for ant in self.ants:
                if ant.wentToRoad(road):
                    deltaPheromone = deltaPheromone + ant.getPheromone()
            
            new_pheromone = self.p * road.getPheromone() + deltaPheromone
            road.setPheromone(new_pheromone)
    
    def shortestRoad(self, roads):
        shortest_road = roads[0]
        for road in roads:
            if road.getDistance() < shortest_road.getDistance():
                shortest_road = road
        return shortest_road

    # Count probability for ant k to move from city i to city j
    # Return the road with the highest probability
    def countProbability(self, ant):
        available_roads = list()
        # Get all the available roads from the current city
        for road in self.all_roads:
            if road.getDistance() > 0:
                if road.city1_id == ant.currentCity or road.city2_id == ant.currentCity:
                    if ant.wentToRoad(road) == False:
                        available_roads.append(road)
        
        # If there are no available roads
        # Get back to the first city
        if not available_roads:
            for road in all_roads:
                if road.city1_id == ant.start_city_id or road.city2_id == ant.start_city_id:
                    return road

        # Count denominator for the equation
        denominator = 0
        #print(len(available_roads))
        for road in available_roads:
            pheromone = road.getPheromone()
            visibility = 1/road.getDistance()
            product = pheromone ** self.alpha * visibility ** self.beta
            denominator = denominator + product

        # When the road has no pheromone
        # Choose the shortest road
        if denominator == 0:
            return self.shortestRoad(available_roads)

        # Count all probabilities
        probabilities = list()
        for road in available_roads:
            pheromone = road.getPheromone()
            visibility = 1/road.getDistance()
            nominator = pheromone ** self.alpha * visibility ** self.beta
            probability = nominator/denominator
            #print(f'Probability: {probability}')
            probabilities.append(probability)

        # Get highest probability
        highest_probability = 0
        index_of_best_road = None
        for i in range(len(probabilities)):
            if probabilities[i] > highest_probability:
                highest_probability = probabilities[i]
                index_of_best_road = i
        
        best_road = available_roads[index_of_best_road]
        return best_road 
    
    # Reset ants memory 
    def resetTravelData(self):
        for ant in self.ants:
            ant.resetTravelData()

    # Run ant colony algorithm step by step
    def runAlgorithm(self):
        for t in range(self.iterations):
            for ant in self.ants:
                for move_count in range(self.cities):
                    new_road = self.countProbability(ant)
                    ant.move(new_road)
                self.updatePheromoneValue()
                ant.showAntDetails()
            # Reset ant memory        
            self.resetTravelData()
        
        #self.showGeneralPheromoneLevel()
    
    def showGeneralPheromoneLevel(self):
        for road in self.all_roads:
            print(f'From {road.city1_id} to {road.city2_id}:')
            print(f'Distance: {road.getDistance()}')
            print(f'Pheromone: {road.getPheromone()}')
            print("---")

    def showFinalResult(self):
        pass
            
if __name__ == "__main__":
    size = 10 # Size of the colony
    iterations = 150 # Expected iterations
    alpha = 10 # Pheromone attraction
    beta = 2 # Short distance attraction
    p = 0.7 # Evaporation constant
    Q = 5 # Ants pheromone constant

    c = Colony(size, iterations, alpha, beta, p, Q)
    c.runAlgorithm()
