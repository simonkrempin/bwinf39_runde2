import random


class Reservation:
    def __init__(self, input_arr):
        self.begin = input_arr[0]
        self.ending = input_arr[1]
        self.length = input_arr[2]
        self.size = self.ending - self.begin

        self.x = -1
        self.y = -1

        self.height_multiplier = 10

        self.bottom_right = (self.length, self.size * self.height_multiplier)
        self.top_left = (self.x, self.begin)

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
