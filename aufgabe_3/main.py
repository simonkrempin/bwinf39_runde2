import random
import individual as idl
import math

# reading the file
file = open("example1.txt")  # change the input file for the algorithm
circumference = int(file.readline().split()[0])
house_positions = list(map(int, file.readline().split()))
approximate_process_times = circumference * len(house_positions)

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


def calc_fitness(chromosome, c_individual) -> int:
    fitness_value = 0
    for index in range(len(house_positions)):
        fitness_value += 1 if population[0].nearest_ip[index] > nearest_ip_for_house(house_positions[index], chromosome) else -1
    return fitness_value


def fitness_function(pop, c_individual):
    # since the comparison changes with each generation the highest is the new comparison
    highest_fitness = 0  # starts at 0 because no -1 is better then comparison value
    for individual in pop:
        individual.fitness_value = calc_fitness(individual.chromosome, c_individual)
        if individual.fitness_value > highest_fitness:
            highest_fitness = individual.fitness_value
            c_individual = individual
    return c_individual


def nearest_ip_for_house(house_position, chromosome) -> int:
    closest: int = circumference
    for gen in chromosome:
        value1 = math.fabs(gen - house_position)
        value2 = math.fabs(gen - circumference - house_position)
        closest = value1 if value1 < value2 and value1 < closest else value2 if value2 < value1 and value2 < closest else closest
    return closest


def determine_mating_pool(population) -> []:
    lowest_fitness = min(list(x.fitness_value for x in population))
    for individual in population[1:]:  # ignore the first individual since its the comparison individual
        individual.fitness_value += math.fabs(lowest_fitness)

    # determine a threshold
    threshold = sum([individual.fitness_value for individual in population]) / len(population)
    mating_pool = []
    for individual in population:
        if individual.fitness_value > threshold:
            mating_pool.append(individual)
    return mating_pool


def crossover_function(individual1, individual2):
    chromosome1 = individual1.chromosome
    chromosome2 = individual2.chromosome
    for gen_index in range(len(chromosome1)):
        if random.randint(0, 1) == 0:
            chromosome1[gen_index], chromosome2[gen_index] = chromosome2[gen_index], chromosome1[gen_index]
    return idl.Individual(chromosome1), idl.Individual(chromosome2)


def crossover(population):
    crossover_population = []
    for x in range(len(population) // 2):
        # get two random genes
        individual1 = population[random.randint(0, len(population) - 1)]
        individual2: idl.Individual

        while True:
            individual2 = population[random.randint(0, len(population) - 1)]
            if individual2 is not individual1:
                break

        individual1, individual2 = crossover_function(individual1, individual2)
        crossover_population.append(individual1)
        crossover_population.append(individual2)
    return crossover_population


def mutate_individual(individual: idl.Individual) -> None:
    for gen_index in individual.chromosome:
        if random.randint(0, 2) == 1:
            while True:
                value = random.randint(0, circumference)

                if value not in individual.chromosome:
                    population[gen_index].chromosome = value
                    break


def mutation(population):
    pos_index = 1
    for individual in population:
        if random.randint(0, pos_index) == 0:
            pos_index += 1
            continue
        pos_index = 1
        mutate_individual(individual)
    return new_population


# evolution loop
comparison_individual = idl.Individual([int(circumference/3), int(circumference/3 * 2), int(circumference)])
repeated_solutions = []
loop_counter = 0

while True:
    new_comparison_value = fitness_function(population, comparison_individual)
    if comparison_individual is not new_comparison_value:
        if new_comparison_value in repeated_solutions:
            break
        repeated_solutions.append(comparison_individual)
        comparison_individual = new_comparison_value
        counter = 0
    new_population = crossover(determine_mating_pool(population))
    mutation(new_population)
    # select survivor

    # loop anchor
    loop_counter += 1

    highest_value = 0
    for individual_index in range(len(population)):
        if comparison_individual.fitness_value < population[individual_index].fitness_value:
            comparison_individual = population[individual_index]

    if loop_counter > approximate_process_times:
        break
print(comparison_individual)
