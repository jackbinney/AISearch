### EXECUTE THE CODE IN PYTHON 3 UPWARDS ###

# Modules necessary
from random import randint
import random
import math

# Change this file name as necessary 
fileName = "AISearchfile017.txt" 
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

def getFitness(tour):
	# Returns the fitness of the tour, the higher the fitness value the better
	return 1/getDistance(tour)

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

def mutation(tour):
	# Gives the tour a 1 in 10 chance of mutating. A mutation is where two random cities within the tour have their positions switched. 
	copy = tour[:]
	if random.random() < 0.1:
		city1Index = randint(0, size - 1)
		city2Index = randint(0, size  - 1)
		while city1Index == city2Index:
			city2Index = randint(0, size - 1)

		city1Value = copy[city1Index]
		city2Value = copy[city2Index]

		copy[city1Index] = city2Value
		copy[city2Index] = city1Value

	return copy

def crossover(parent1, parent2):
	# Combines two parents to make a child

	crossoverSize = randint(3, len(parent1) - 1)
	start = randint(0, size - crossoverSize - 1)

	# This produces a toursegment to be directly transferred from parent1 into the child
	crossoverArray = []
	for i in range(0, crossoverSize):
		crossoverArray.append(parent1[start + i])

	# The child is then produced by adding all cities in parent2 that is not in the crossoverArray up until the start of the crossoverArray in...
	# parent1. Then the crossoverArray is added into the child. Then all remaining elements in parent2 are added into the child tour. 
	child = []
	for i in range(0, size):
		if parent2[i] not in crossoverArray:
			child.append(parent2[i])
	for i in range(0, len(crossoverArray)):
		child.insert(start + i, crossoverArray[i])

	# Catches any possible errors where the child is not the same length as the parent
	if len(child) != len(parent1):
		crossover(parent1, parent2)
	else:
		return child

def getFittest(population):
	# Loops through the population and finds the fittest of them
	fittest = 0
	for i in range(0, len(population)):
		if getFitness(population[fittest]) <= getFitness(population[i]):
			fittest = i
	return fittest

def orderPopulationByFitness(population):
	# Reorders the population array to have the fittest tour at the start and the least fit tour at the end
	copy = population[:]
	ordered = []
	populationSize = len(copy)
	while len(ordered) != populationSize:
		fittest = copy[getFittest(copy)]
		ordered.append(fittest)
		copy.remove(fittest)
	return ordered

"""
def evolvePopulation(population):
	populationSize = len(population)

	newPopulation = []
	for i in range(0, populationSize):
		mate = randint(0, populationSize - 1)
		while mate == i:
			mate = randint(0, populationSize - 1)

		child = crossover(population[i], population[mate])
		while(child == None):
			child = crossover(population[i], population[mate])
		newPopulation.append(child)
	
	for i in range(0, populationSize):
		newPopulation[i] = mutation(newPopulation[i])

	return newPopulation
"""

def modifiedEvolvePopulation(population):
	populationSize = len(population) - 1

	newPopulation = []
	orderedPopulation = orderPopulationByFitness(population)
	# Produces a selection of tours that are allowed to produce a child
	rand = randint(1, populationSize)
	for i in range(0, populationSize + 1):

		# parent1 and 2 are a random tours within the selected tours
		parent1 = randint(0, rand)
		parent2 = randint(0, rand)
		# Ensures that the two parents are not the same
		while parent1 == parent2:
			parent2 = randint(0, rand)

		# Produces a child and adds it to the new population
		child = crossover(orderedPopulation[parent1], orderedPopulation[parent2])
		while (child == None):
			child = crossover(orderedPopulation[parent1], orderedPopulation[parent2])
		newPopulation.append(child)

	# Loops through the new population and gives it a chance to mate
	for i in range(0, populationSize):
		newPopulation[i] = mutation(newPopulation[i])

	return newPopulation

def genetic(evolutions):
	# Sets the amount of tours within the population
	populationSize = 100
	population = []

	# Initialises the starting population
	for i in range(0, populationSize):
		population.append(createRandomTour())

	# Loops through and evolves the population by the specified amount of evolutions, storing the best tour found amongst all populations
	best = population[getFittest(population)]
	for i in range(0, evolutions):
		newPopulation = modifiedEvolvePopulation(population)
		bestNew = getFittest(newPopulation)
		if getFitness(best) < getFitness(newPopulation[bestNew]):
			best = newPopulation[bestNew]
			print(getDistance(best))
		# Sets the current population to be the newPopulation
		population = newPopulation
	print(best, getDistance(best))

	return bumpUp(best), getDistance(best)

def bumpUp(tour):
	temp = []
	for city in tour:
		temp.append(city + 1)

	return temp

genetic(1000)