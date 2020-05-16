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

    # Define when 2 objects are equal
    def __eq__(self, other):
        if self.city1_id == other.city1_id and self.city2_id == other.city2_id:
            return True
        elif self.city2_id == other.city1_id and self.city1_id == other.city2_id:
            return True
        else:
            return False

    # Make object hashable
    def __hash__(self):
        return hash(('city1', self.city1_id, 'city2', self.city2_id, 'distance', self.distance))
    
    def showRoadData(self):
        print('---')
        print(f'Distance: {self.distance}')
        print(f'From: {self.city1_id}')
        print(f'To: {self.city2_id}')
        print(f'Pheromone: {self.pheromone}')
    
    # Check if this road belongs to given city
    def belongsToCity(self, city_id):
        if self.city1_id == city_id or self.city2_id == city_id:
            return True
        return False
    
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
        self.cities.append(self.currentCity)

    def resetTravelData(self):
        self.roads = list()
        self.cities = list()
        self.totalDistance = 0
    
    # Move along the road
    def move(self, road):
        #print(f'Start city: {self.start_city_id}')
        #print(f'Current city: {self.currentCity}')
        # Add distance of this road to total distance
        addDistance = road.getDistance()
        self.totalDistance = self.totalDistance + addDistance
        
        newCity = road.city1_id
        if newCity == self.currentCity:
            newCity = road.city2_id
        
        # Change the current city
        self.currentCity = newCity

        # Remember this city as already visited
        self.cities.append(self.currentCity)

        # Add this road to already used
        self.roads.append(road)
    
    def showAntDetails(self):
        print(f'Pheromone: {self.Qpheromone}')
        print(f'Begin city: {self.start_city_id}')
        print(f'Total distance: {self.totalDistance}')
        #print(f'Current city: {self.currentCity}')
        roads_string = ''
        for road in self.roads: 
            roads_string = roads_string + str(road.getDistance()) + ' -> '
        
        cities_string = ''
        for city in self.cities:
            cities_string = cities_string + str(city) + ' -> '
        
        print(f'Distances: {roads_string}')
        print(f'Cities: {cities_string}')
        print("---")

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
        
        self.removeRoadDuplicates()

    def removeRoadDuplicates(self):
        self.all_roads = list(dict.fromkeys(self.all_roads))
        
        #for road in self.all_roads:
        #    road.showRoadData()
    
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
        
        #print(f'Taking shortest road: {shortest_road.city1_id} - {shortest_road.city2_id} ({shortest_road.getDistance()})')
        return shortest_road

    # Return all the roads the ant can take
    def getAvailableRoads(self, ant):
        available_roads = list()
        for road in self.all_roads:
            if ant.wentToRoad(road) == False:
                if ant.currentCity == road.city1_id and ant.wentToCity(road.city2_id) == False:
                    available_roads.append(road)
                elif ant.currentCity == road.city2_id and ant.wentToCity(road.city1_id) == False:
                    available_roads.append(road)
        return available_roads


    # Count probability for ant k to move from city i to city j
    # Return the road with the highest probability
    def countProbability(self, ant):
        available_roads = self.getAvailableRoads(ant)
        
        # If there are no available roads
        # Get back to the first city
        if not available_roads:
            for road in self.all_roads:
                if road.city1_id == ant.start_city_id and road.city2_id == ant.currentCity:
                    #print(f'Start City: {ant.start_city_id}')
                    #print(f'Current city: {ant.currentCity}')
                    return road
                elif road.city2_id == ant.start_city_id and road.city1_id == ant.currentCity:
                    #print(f'Start City: {ant.start_city_id}')
                    #print(f'Current city: {ant.currentCity}')
                    return road

        ### --- SHOW AVAILABLE ROADS --- ####
        #print('---')
        #print('AVAILABLE ROADS')
        #for road in available_roads:
        #    road.showRoadData()
        ### --- SHOW AVAILABLE ROADS --- ####

        # Count denominator for the equation
        denominator = 0
        #print(len(available_roads))
        for road in available_roads:
            pheromone = road.getPheromone()
            visibility = 1/road.getDistance()
            product = pheromone ** self.alpha * visibility ** self.beta
            denominator = denominator + product
        
        ### --- DENOMINATOR --- ###
        #print(f'Denominator for this ants roads: {denominator}')
        ### --- DENOMINATOR --- ###

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
        
        ### --- PROBABILITIES FOR ROADS --- ###
        #print('Probabilities for roads')
        #print(f'{probabilities}')
        ### --- PROBABILITIES FOR ROADS --- ###

        # Get highest probability
        highest_probability = 0
        index_of_best_road = None
        for i in range(len(probabilities)):
            if probabilities[i] > highest_probability:
                highest_probability = probabilities[i]
                index_of_best_road = i
        
        ### --- Highest probability and best index --- ###
        #print(f'Best Probability: {highest_probability}, index: {index_of_best_road}')
        ### --- Highest probability and best index --- ###

        best_road = available_roads[index_of_best_road]

        ### --- BEST ROAD INFO --- ###
        #print('BEST ROAD INFO')
        #best_road.showRoadData()
        ### --- BEST ROAD INFO --- ###

        return best_road 
    
    # Reset ants memory 
    def resetTravelData(self):
        for ant in self.ants:
            ant.resetTravelData()

    # Run ant colony algorithm step by step
    def runAlgorithm(self):
        start = time.time()
        for t in range(self.iterations):
            for ant in self.ants:
                for move_count in range(self.cities):
                    new_road = self.countProbability(ant)
                    ant.move(new_road)
            
            self.updatePheromoneValue()
            # Reset ant memory        
            self.resetTravelData()
        
        end = time.time()
        #self.showGeneralPheromoneLevel()
        self.showFinalResult()
        timeInSeconds = round(end-start,2)
        print(f'Time: {timeInSeconds} s')
    
    def showGeneralPheromoneLevel(self):
        for road in self.all_roads:
            print(f'From {road.city1_id} to {road.city2_id}:')
            print(f'Distance: {road.getDistance()}')
            print(f'Pheromone: {road.getPheromone()}')
            print("---")

    # Show final path
    def showFinalResult(self, city_id=None):
        if city_id == None:
            city_id = 0
        
        final_roads = list()

        for i in range(self.cities):
            roads_to_city = list()
            # Get all the roads related to this city
            for road in self.all_roads:
                # check if road belongs to city and was not already taken
                if road.belongsToCity(city_id) and not road in final_roads:
                    roads_to_city.append(road)
            
            # Find one with highest amount of pheromone
            highest_pheromone = 0
            best_road = None
            for road in roads_to_city:
                if road.getPheromone() > highest_pheromone:
                    highest_pheromone = road.getPheromone()
                    best_road = road

            # Save road into final path
            final_roads.append(best_road)

            # Change city for a new one city_id
            if best_road.city1_id == city_id:
                city_id = best_road.city2_id
            elif best_road.city2_id == city_id:
                city_id = best_road.city1_id

        # Display the way and total distance
        totalDistance = 0
        for road in final_roads:
            #road.showRoadData()
            totalDistance = totalDistance + road.getDistance()
            print(f'{road.getDistance()} -> ', end='')
        print(f'Total: {totalDistance}')
            
if __name__ == "__main__":
    size = 10 # Size of the colony
    iterations = 3 # Expected iterations
    alpha = 100 # Pheromone attraction
    beta = 5 # Short distance attraction
    p = 0.5 # Evaporation constant
    Q = 5 # Ants pheromone constant

    c = Colony(size, iterations, alpha, beta, p, Q)
    c.runAlgorithm()
