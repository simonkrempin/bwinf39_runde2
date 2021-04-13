# --------- GA to solve an optimization problem ----------
import random
import individual as idl
import math

# reading the file
file = open("example1.txt")  # change the input file for the algorithm
circumference = int(file.readline().split()[0])
last_pos = circumference - 1  # -1 for the last number of the circle
house_positions = list(map(int, file.readline().split()))
pop_size = 40
lt_threshold = circumference


# define the length of the chromosome by the users input
chr_length = 3
while True:
    try:
        chr_length = int(input())
        if circumference > chr_length > 0:
            break
    except ValueError:
        pass
    print('please enter an 0 < x < circumference')
    print(f'the circumference is %s' % circumference)


# ---------- define fitness for pop -------------
def calc_nearest_ip(chromosome, house_posses) -> []:
    arr = []
    for house_pos in house_posses:
        nearest = last_pos
        for gen in chromosome:
            value1 = math.fabs(house_pos - gen)
            value2 = math.fabs((last_pos + 1) - value1)
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
    # for individual in pop:
    #    threshold += individual.fitness_value
    # threshold /= len(pop)

    return_pop = []
    for individual in pop:
        if individual.fitness_value >= threshold:
            return_pop.append(individual)
    return return_pop


# ------------ crossover function ---------------
def crossover_function(pop) -> []:
    if len(pop) <= 0:
        return []
    lowest_value = min([individual.fitness_value for individual in pop])

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
    # return if c1 or c2 are None with a random new individual
    if c1 is None and c2 is None:
        return idl.Individual(random.sample(range(0, last_pos), chr_length)), idl.Individual(random.sample(range(0, last_pos), chr_length))
    elif c1 is None:
        return idl.Individual(random.sample(range(0, last_pos), chr_length)), c2
    elif c2 is None:
        return c1, idl.Individual(random.sample(range(0, last_pos), chr_length))

    for index in range(len(c1.chromosome)):
        if random.randint(0, 1) == 0:
            c2.chromosome[index], c1.chromosome[index] = c1.chromosome[index], c2.chromosome[index]

    # chromosome might contain duplicate through crossover and then the chromosome is no valid chromosome -> remove invalid chromosomes
    if len(c1.chromosome) != len(set(c1.chromosome)):
        c1 = idl.Individual(random.sample(range(0, last_pos), chr_length))
    if len(c2.chromosome) != len(set(c2.chromosome)):
        c2 = idl.Individual(random.sample(range(0, last_pos), chr_length))

    return c1, c2


# ----------- mutate chromosomes -----------
def mutation(pop):
    probability = 1
    for individual in pop[:-1]:
        if random.randint(0, 1) == 0:
            probability += 1
            continue
        individual.chromosome = mutate_chromosome(individual)
        probability = 1  # reset probability after mutation
    return pop


def mutate_chromosome(individual):
    for gen_index in range(len(individual.chromosome)):
        if random.randint(0, 1) == 0:
            while True:
                rnd_v = random.randint(0, last_pos)
                if rnd_v not in individual.chromosome:
                    individual.chromosome[gen_index] = rnd_v
                    break
    return individual.chromosome


def create_initial_population(comparison_idl, population):
    for value in range(40):
        population.append(idl.Individual(random.sample(range(0, last_pos), chr_length)))

    if chr_length > len(house_positions):
        other_values = [_ for _ in range(0, last_pos) if _ not in house_positions]
        comparison_idl.chromosome = house_positions + random.sample(other_values, chr_length - len(house_positions))
    else:
        comparison_idl.chromosome = random.sample(house_positions, chr_length)


def solution_in_solutions(solution, solutions):
    for s in solutions:
        if s.chromosome[0] in solution.chromosome and s.chromosome[1] in solution.chromosome and s.chromosome[2] in solution.chromosome:
            return True
    return False


# ----------- Genetic Algorithm ------------
population = []
solutions = []
solution = idl.Individual('I hope you have a beautiful day because i did not have one')
create_initial_population(solution, population)

lt = 0

while True:
    fitness_function(population, solution)
    mating_pool = create_mating_pool(population)
    offspring = crossover_function(mating_pool)

    # find the best individual from the population
    hf_individual = None
    for individual in population:
        if hf_individual is None or hf_individual.fitness_value < individual.fitness_value:
            hf_individual = individual
    if hf_individual is not None and hf_individual.fitness_value > 0:
        solution = hf_individual

    m_offspring = mutation(offspring)

    if len(solutions) > 0 and solution is solutions[-1]:
        lt += 1
    elif solution_in_solutions(solution, solutions):
        lt = lt_threshold
    else:
        solutions.append(solution)
        lt = 0

    population = m_offspring
    while len(population) < 39:
        population.append(idl.Individual(random.sample(range(0, last_pos), chr_length)))
    if hf_individual is not None and hf_individual.fitness_value > 0:
        population.append(solution)

    if lt >= lt_threshold:
        break
print(solution.chromosome)
