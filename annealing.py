# Simulated annealing algorithm
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

# Class representing City
class City(object):
    def __init__(self, _id, distances):
        self._id = _id
        self.distances = distances
    
    def getId(self):
        return self._id

    # Returns a distance from this city to city with id=city_id
    def getDistance(self, city_id):
        return self.distances[city_id]
    
    def setRoads(self, roads):
        self.roads = roads

    def showDistances(self):
        print(self.distances)

# Class made for Simulated Annealing Algorithm
class Annealing(object):
    def __init__(self, Tmax, Tmin, Tstep):
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.Tstep = Tstep
        self.cities = list()
        self.initCitiesFromFile()

    def initCitiesFromFile(self):
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
            
            city = City(row-1, distances)
            self.cities.append(city)
                    
    def showCities(self, cities_list=None):
        if cities_list == None:
            cities_list = self.cities

        for city in cities_list:
            print(city.getId())
            city.showDistances()

    # Calculate total distance between all the cities in current case
    def calculateTotalDistance(self, cities_list=None):
        if cities_list == None:
            cities_list = self.cities

        totalDistance = 0

        road = ''

        for i in range(len(cities_list)):
            if i == len(cities_list)-1:
                next_city_id = cities_list[0].getId() 
                totalDistance = totalDistance + cities_list[i].getDistance(next_city_id)

                road = road + str(cities_list[i].getDistance(next_city_id))
            else:
                next_city_id = cities_list[i+1].getId()
                totalDistance = totalDistance + cities_list[i].getDistance(next_city_id)

                road = road + str(cities_list[i].getDistance(next_city_id)) + ' -> '
        
        road = road + f' ({totalDistance})'
        print(road)
        return totalDistance
    
    # Switches 2 randomly chosen cities in the list
    # And returns a copy of this list (NOT CHANGING THE MAIN LIST)
    def switchCities(self):
        cities_amount = len(self.cities)
        index1 = random.randrange(cities_amount)
        index2 = random.randrange(cities_amount)

        cities_buffer = self.cities.copy()

        while index2 == index1:
            index2 = random.randrange(cities_amount)

        tmp = cities_buffer[index1]
        cities_buffer[index1] = cities_buffer[index2]
        cities_buffer[index2] = tmp

        return cities_buffer
    
    # Go through annealing algorithm
    def anneal(self):
        # Find random way between the cities
        random.shuffle(self.cities)
        currentDistance = 0 
        
        for temperature in range(self.Tmax, self.Tmin, -self.Tstep):
            sp.call('clear',shell=True)

            currentDistance = self.calculateTotalDistance()
            #print(f"Current Distance: {currentDistance}")
            next_combination = self.switchCities()
            
            nextDistance = self.calculateTotalDistance(next_combination)
            #print(f"Next distance: {nextDistance}")
            
            difference = nextDistance - currentDistance
            #print(f'Difference: {difference}')


            if difference < 0:
                currentDistance = nextDistance
                self.cities = next_combination.copy()
            elif math.exp(-difference/temperature) > random.random():
                currentDistance = nextDistance
                self.cities = next_combination.copy()
                percent = math.exp(-difference/temperature) * 100
                percent = round(percent, 2)
                #print(f'Temp: {temperature}')
                #print(f'% chance: {percent}%')
            
            #time.sleep(0.1)

        print(f'Distance found: {currentDistance}')
        #self.showCities()

A = Annealing(1000,5,5)
A.anneal()
