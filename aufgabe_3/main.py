# --------- GA to solve an optimization problem ----------
import random
import individual as idl
import math

# reading the file
file = open("example1.txt")  # change the input file for the algorithm
circumference = int(file.readline().split()[0])
house_positions = list(map(int, file.readline().split()))
approximate_processing_times = circumference * 3

# ----------------- GA ---------------
looping_times = 0
# create initial population
while True:
    # fitness function
    # set the new comparison individual
    # mating pool
    # crossover function
    # mutation
    # loop anchor

    if looping_times >= approximate_processing_times:
        break
