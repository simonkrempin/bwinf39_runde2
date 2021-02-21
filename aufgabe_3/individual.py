class Individual:
    def __init__(self, chromosome):
        self.fitness_value: int = 0
        self.chromosome = chromosome
        self.nearest_ip = []
