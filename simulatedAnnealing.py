### EXECUTE THE CODE IN PYTHON 3 UPWARDS ###

# Modules necessary
from random import randint
import random
import math

# Change this file name as necessary 
fileName = "AISearchfile012.txt" 
# Opens the file, strips it of spaces and splits by commas
file = open(fileName, 'r')
fileContents = file.read()
fileContents = [x.strip() for x in fileContents.split(",")]
# Necessary to ensure that the counter used below doesn't throw an error
fileContents.append("0");
# Saves the tour size of the file
size = int(fileContents[1].replace("SIZE = ", ""))

# Initialises an array to store the distances between cities
distances = []
counter = 0
# Loop through adding each city's connections to the distances array
for i in range(0, size):
	row = []
	for j in range(0, size):
		# This is the next distance to be added to the array if it is not already in there
		distance = fileContents[2 + counter]
		# Checks for noise within the distance, if the distance contains symbols/letters of the alphabet, remove it
		if not distance.isdigit():
			newString = ""
			for character in distance:
				if character.isdigit():
					newString = newString + character
			distance = int(newString)

		# If the row is greater than the column, the distance has already been added, therefore just needs mirroring
		if (i > j):
			row.append(int(distances[j][i]))
		# If the cities are equal to one another, the distance between them is 0
		elif (i == j):
			row.append(0)
		# If the row is less than the column, the distance has not yet been added, find the next distance to be added and add it
		else:
			row.append(int(distance))
			counter = counter + 1
	# Add the city's connections to the distances array
	distances.append(row)

def getDistance(tour):
	# Loop through the tour, find the distance in the distances array and add it to the total distance
	distance = 0
	i = 0
	j = 1
	while j < len(tour):
		distance = distance + distances[tour[i]][tour[j]]
		i = i + 1
		j = j + 1

	distance = distance + distances[tour[len(tour) - 1]][tour[0]]
	return distance

def createRandomTour():
	# Produces a random tour by adding all cities within the tour file, then adding them to the tour at random as long as they are currently...
	# not already in the tour
	unvisited = []
	tour = []
	for i in range(0, size):
		unvisited.append(i)
	
	while len(tour) != size:
		rand = randint(0, len(unvisited) - 1)
		tour.append(unvisited[rand])
		unvisited.remove(unvisited[rand])

	return tour

def createRandomNeighbourTour(tour):
	# Creates a neighbouring tour by selecting a random start and end position within the tour and randomising the cities in between the start...
	# and end positions

	start = randint(0, size - 1)
	end = randint(start, size - 1)
	while (end - start) <= 2:
		start = randint(0, size - 1)
		end = randint(start, size - 1)
	
	unvisited = []
	newTour = []
	distance = 0
	for i in range(0, start):
		newTour.append(tour[i])
	for i in range(start, end):
		unvisited.append(tour[i])
	while len(unvisited) != 0:
		rand = randint(0, len(unvisited) - 1)
		newTour.append(unvisited[rand])
		unvisited.remove(unvisited[rand])
	for i in range(end, size):
		newTour.append(tour[i])

	return newTour

def createNeighbourTour(tour):
	# Creates a neighbouring tour by selecting two cities at random in the tour and switching their positions
	copy = tour[:]
	city1Index = randint(0, size - 1)
	city2Index = randint(0, size - 1)
	while city1Index == city2Index:
		city2Index = randint(0, size - 1)

	city1Value = copy[city1Index]
	city2Value = copy[city2Index]

	copy[city1Index] = city2Value
	copy[city2Index] = city1Value

	return copy

def createReverseNeighbourTour(tour):
	# Creates a neighbouring tour by selecting a random start and end position from within the tour and reversing the order between these two...
	# points.
	start = randint(0, size - 1)
	end = randint(start, size - 1)
	while (end - start) <= 2:
		start = randint(0, size - 1)
		end = randint(start, size - 1)
	
	unvisited = []
	newTour = []
	distance = 0
	for i in range(0, start):
		newTour.append(tour[i])
	for i in range(start, end):
		unvisited.append(tour[i])
	while len(unvisited) != 0:
		newTour.append(unvisited[len(unvisited) - 1])
		unvisited.remove(unvisited[len(unvisited) - 1])
	for i in range(end, size):
		newTour.append(tour[i])

	return newTour

def acceptance(tour1, tour2, temp):
	# Determines whether a newTour should be taken as the new current tour. If the new tour is better than the old tour, return 1, else return an...
	# exponential of the two tours
	if getDistance(tour2) < getDistance(tour1):
		return 1.0
	else:
		value = math.exp(-(getDistance(tour2) - getDistance(tour1)) / temp)
		return value

def sA():
	# Sets the temperature and coolingRate of the simulated annealing algorithm, feel free to change this accordingly
	temp = 10000000
	coolingRate = 0.0001

	# Creates a tour to start with
	bestTour = createRandomTour()
	bestDistance = getDistance(bestTour)
	currentTour = bestTour
	# While the temperature has not hit 1, create possible tours, potentially make them the new current tour based on the acceptance value produced...
	# Higher temperatures result in higher acceptance values and therefore worse tours are taken into consideration. If the currentTour is better...
	# Than the best tour found, replace it. Then reduce the temperature.
	while temp > 1:
		possibleTour = createReverseNeighbourTour(currentTour)
		
		if (acceptance(currentTour, possibleTour, temp) > random.random()):
			currentTour = possibleTour 

		if (getDistance(currentTour) < bestDistance):
			bestTour = currentTour
			bestDistance = getDistance(bestTour)
			print(bestDistance)

		temp = temp * (1-coolingRate)
	return bumpUp(bestTour), bestDistance

def bumpUp(tour):
	temp = []
	for city in tour:
		temp.append(city + 1)

	return temp

print(sA())
