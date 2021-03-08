# imports
import math
import random


class House:
    def __init__(self, position):
        self.position = position
        self.closest: int = circumference

    def shortest_distance_house_position(self, positions_ice):
        temp_closest: int = circumference
        for temp in positions_ice:
            value1 = math.fabs(self.position - temp)
            value2 = math.fabs(self.position + circumference - temp)
            temp_closest = value2 if value2 < value1 and value2 < temp_closest else value1 if value1 < temp_closest else temp_closest
        return temp_closest


if __name__ == '__main__':
    # reading the file
    file = open("example1.txt")
    circumference = int(file.readline().split()[0])
    house_positions = file.readline().split()

    houses = []
    for p in house_positions:
        houses.append(House(int(p)))

    # genetic algorithm
    alg_times = circumference * 5

    # setup the starting position for the ice stands
    # differ this value to check if solution is right
    comparison_ice_pos = [12, 16, 4]
    comparison_house_nearest = []
    for h in houses:
        comparison_house_nearest.append(int(h.shortest_distance_house_position(comparison_ice_pos)))

    # initial random generated positions
    generation = []
    for i in range(100):
        generation.append(random.sample(range(circumference + 1), 3))

    fitness_values = []
    for iteration in range(alg_times):
        # calculate the fitness of each gen of the current generation
        # comparison value is the best value from the last generation if it was positive
        fitness_values = []
        for gen in generation[1:]:
            votes = 0
            for house_pos in range(len(houses)):
                votes += 1 if houses[house_pos].shortest_distance_house_position(gen) < comparison_house_nearest[house_pos] else -1
            fitness_values.append([votes, gen])

        # evaluation
        # add the two highest values the the next generation
        first = [-20000, None]
        second = [-20000, None]
        for value in fitness_values:
            if value[0] > second[0]:
                if value[0] > first[0]:
                    first, second = value, first
                else:
                    second = value
        first_value = first[0]
        new_generation = [first[1], second[1]]

        # to select gens and compare them translate minus into positive values
        anti_minus_value = math.fabs(min(fitness_values)[0]) + 1
        evaluation_fitness_values = [(element[0] + anti_minus_value) * 10 for element in fitness_values]  # change the multiplication value for boosting/nerf the better gens by higher/lower the value
        fitness_range = sum(evaluation_fitness_values)

        # cross genes of current generation
        for i in range(40):  # change this value if more gens should get crossed > makes 80 new gens
            # get first gen
            random_value = random.randint(0, fitness_range)
            first_array_index = -1
            while random_value > 0:
                first_array_index += 1
                random_value -= evaluation_fitness_values[first_array_index]

            # get second gen
            second_array_index = -1
            while first_array_index == second_array_index or second_array_index == -1:  # that the gens don't double
                random_value = random.randint(0, fitness_range)
                second_array_index = -1
                while random_value > 0:
                    second_array_index += 1
                    random_value -= evaluation_fitness_values[second_array_index]

            # cross the two gens
            split_beginning = random.randint(1, 3)
            split_ending = random.randint(split_beginning, 3)
            first_gen = generation[first_array_index]
            second_gen = generation[second_array_index]
            first_crossed_gen = None
            second_crossed_gen = None
            # not a pretty solution
            if split_beginning == 1 and split_ending == 2:
                first_crossed_gen = [first_gen[0], second_gen[1], second_gen[2]]
                second_crossed_gen = [second_gen[0], first_gen[1], first_gen[2]]
            elif split_beginning == 1 and split_ending == 1:
                first_crossed_gen = [first_gen[0], second_gen[1], first_gen[2]]
                second_crossed_gen = [second_gen[0], first_gen[1], second_gen[2]]
            else:
                first_crossed_gen = [first_gen[0], first_gen[1], second_gen[2]]
                second_crossed_gen = [second_gen[0], second_gen[1], first_gen[2]]
            new_generation.append(first_crossed_gen)
            new_generation.append(second_crossed_gen)

        # mutate random gens by changing a pos to a random value
        current_index = 1
        while current_index < len(new_generation) - 1:
            current_index += random.randint(1, len(new_generation) - current_index - 1)
            mutation_gen = new_generation[current_index]

            strand_index = random.randint(0, 2)
            mutation_pos = random.randint(0, circumference)
            while mutation_pos == mutation_gen[0] and mutation_pos == mutation_gen[1] and mutation_pos == mutation_gen[2]:  # prevent doubled positions
                mutation_pos = random.randint(0, circumference)
            mutation_gen[strand_index] = mutation_pos
            new_generation[current_index] = mutation_gen

        # if a better version is found overwrite the current comparison with the better version
        generation = new_generation
        if first_value > 0:
            comparison_house_nearest = []
            comparison_ice_pos = generation[0]
            for h in houses:
                comparison_house_nearest.append(int(h.shortest_distance_house_position(comparison_ice_pos)))

    print(comparison_ice_pos)
