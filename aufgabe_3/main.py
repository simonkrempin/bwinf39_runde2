# --------- GA to solve an optimization problem ----------
import random
import individual as idl
import math

# reading the file
file = open("example1.txt")  # change the input file for the algorithm
circumference = int(file.readline().split()[0]) - 1  # -1 for the last number of the circle
house_positions = list(map(int, file.readline().split()))
pop_size = 40
alt = circumference * 3


# define the length of the chromosome by the users input
chr_length = 3
while True:
    try:
        chr_length = int(input())
        if circumference >= chr_length > 0:
            break
    except ValueError:
        pass
    print('please enter an 0 < x < circumference')


# ------------- GA Methods ----------------
def create_random_array(length=3, arr=[]) -> []:
    if circumference > length <= 0:
        return arr

    arr = create_random_array(length - 1, arr)

    while True:
        value = random.randint(0, circumference)
        if value not in arr:
            arr.append(value)
            return arr


# ---------- define fitness for pop -------------
def calc_nearest_ip(chromosome, house_posses) -> []:
    arr = []
    for house_pos in house_posses:
        nearest = circumference
        for gen in chromosome:
            value1 = math.fabs(house_pos - gen)
            value2 = math.fabs((circumference + 1) - value1)
            nearest = value1 if value2 > value1 < nearest else value2 if value2 < nearest else nearest
        arr.append(nearest)
    return arr


def compare_two_chromosomes(c1, c2) -> int:
    value = 0
    for i in range(len(c1)):
        value += 1 if c1[i] < c2[i] else -1
    return value


def fitness_function(pop, comp_idl: idl.Individual) -> None:
    comp_idl.nearest_ip = calc_nearest_ip(comp_idl.chromosome, house_positions)
    for individual in pop:
        if individual is comp_idl:
            individual.fitness_value /= 2
        individual.fitness_value = compare_two_chromosomes(calc_nearest_ip(individual.chromosome, house_positions), comp_idl.nearest_ip)


# ------------ create mating pool --------------
def create_mating_pool(pop) -> []:
    threshold = 0
    for individual in pop:
        threshold += individual.fitness_value
    threshold /= len(pop)

    return_pop = []
    for individual in pop:
        if individual.fitness_value >= threshold:
            return_pop.append(individual)
    return return_pop


# ------------ crossover function ---------------
def crossover_function(pop) -> []:
    lowest_value = min([x.fitness_value for x in pop])

    overall_score = 0
    for individual in pop:
        individual.fitness_value += math.fabs(lowest_value)
        overall_score += individual.fitness_value

    return_pop = []
    for _ in range(len(pop) // 2):
        v1 = random.randint(0, overall_score)
        v2 = random.randint(0, overall_score)
        c1 = None
        c2 = None

        for individual in pop:
            if v1 > 0:
                v1 -= individual.fitness_value
                if v1 <= 0:
                    c1 = individual
            if v2 > 0:
                v2 -= individual.fitness_value
                if v2 <= 0:
                    c2 = individual

            if v1 <= 0 and v2 <= 0:
                break

        c1, c2 = cross_chromosomes(c1, c2)
        return_pop.append(idl.Individual(c1.chromosome))
        return_pop.append(idl.Individual(c2.chromosome))
    return return_pop


def cross_chromosomes(c1, c2):
    if c1 and c2 is None:
        return idl.Individual(create_random_array(chr_length, [])), idl.Individual(create_random_array(chr_length, []))
    if c1 is None:
        return idl.Individual(create_random_array(chr_length, [])), c2
    elif c2 is None:
        return c1, idl.Individual(create_random_array(chr_length, []))

    for index in range(len(c1.chromosome)):
        if random.randint(0, 1) == 0:
            c2.chromosome[index], c1.chromosome[index] = c1.chromosome[index], c2.chromosome[index]
    return c1, c2


# ----------- mutate chromosomes -----------
def mutation(pop):
    probability = 1
    for individual in pop[:-1]:
        if random.randint(0, 1) == 0:
            probability += 1
            continue
        individual = mutate_chromosome(individual)
        probability = 1  # reset probability after mutation
    return pop


def mutate_chromosome(individual):
    for gen_index in range(len(individual.chromosome)):
        if random.randint(0, 1) == 0:
            while True:
                rnd_v = random.randint(0, circumference)
                if rnd_v not in individual.chromosome:
                    individual.chromosome[gen_index] = rnd_v
                    break
    return individual


# ----------- Genetic Algorithm ------------
population = []
for _ in range(pop_size):
    population.append(idl.Individual(create_random_array(chr_length, [])))  # create a initial population with random chromosomes

comparison_idl = idl.Individual([6, 2, 14])
solutions = []
lt = 0
looping = True
while looping:
    fitness_function(population, comparison_idl)
    mating_pool = create_mating_pool(population)
    offspring = crossover_function(mating_pool)

    # append the best chromosome to the next population to not lose progress
    chr_highest_fitness = None
    highest_fitness = 0
    for x in population:
        if x.fitness_value > highest_fitness:
            highest_fitness = x.fitness_value
            chr_highest_fitness = x
    if chr_highest_fitness is not None:
        offspring.append(chr_highest_fitness)

    m_offspring = mutation(offspring)

    if chr_highest_fitness is not None:
        comparison_idl = chr_highest_fitness

    if len(solutions) > 0 and solutions[-1] is comparison_idl:
        lt = 0  # if new solution found more processing times
    else:
        lt += 1
        for solution in solutions:
            if comparison_idl.chromosome[0] in solution.chromosome and comparison_idl.chromosome[1] in solution.chromosome and comparison_idl.chromosome[2] in solution.chromosome:
                looping = False
                break
    solutions.append(comparison_idl)

    if lt >= alt:
        looping = False
        break
print(comparison_idl.chromosome)
