import random
import individual as idl
import math

# reading the file
file = open("example1.txt")  # change the input file for the algorithm
circumference = int(file.readline().split()[0])
house_positions = list(map(int, file.readline().split()))
process_times = 1  # circumference * house_positions


def gra(arr=[]):  # generate random array
    if circumference < 2 > len(arr):
        return arr

    while True:
        value = [random.randint(0, circumference)]
        if value[0] not in arr:
            return arr + value


# genetic algorithm
# create a initial population with random values
# each population contains 40 chromosomes with 3 genes
population = []
for i in range(40):
    population.append(idl.Individual(gra(gra(gra()))))


def fitness_function(chromosome):
    f_value = 0
    for index in range(len(house_positions)):
        f_value += 1 if population[0].nearest_ip[index] > nearest_ip_for_house(house_positions[index], chromosome) else -1
    return f_value


def nearest_ip_for_house(house_position, chromosome) -> int:
    closest: int = circumference
    for gen in chromosome:
        value1 = math.fabs(gen - house_position)
        value2 = math.fabs(gen - circumference - house_position)
        closest = value1 if value1 < value2 and value1 < closest else value2 if value2 < value1 and value2 < closest else closest
    return closest


# evolution loop
for i in range(process_times):
    # determine nearest of the best population
    # fitness determine
    for house in house_positions:
        population[0].nearest_ip.append(nearest_ip_for_house(house, population[0].chromosome))
    for individual in population[1:]:
        individual.fitness_value = fitness_function(individual.chromosome)
        
