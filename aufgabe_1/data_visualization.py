import pygame
import random


# data visualization for the rectangles
class DataVisualization:
    def __init__(self, reservations):
        self.reservations = reservations
        self.screen = None

        self.height_multiplier = 10
        self.width_multiplier = 1

        self.create_window(1000 * self.width_multiplier, 10 * self.height_multiplier)
        self.draw_reservations()
        self.action_loop()

    def create_window(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()

    def draw_reservations(self):
        current_x = 0
        for reservation in self.reservations:
            if reservation.x == -1:
                y_coordinate = (reservation.begin - 8) * self.height_multiplier
                height = (reservation.ending - reservation.begin) * self.height_multiplier
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                print(color)
                pygame.draw.rect(self.screen, color, (current_x, y_coordinate, reservation.length, height), 0)
            current_x += reservation.length
        pygame.display.flip()

    def action_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
