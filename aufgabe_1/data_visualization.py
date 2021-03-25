import pygame

# data visualization for the rectangles
class DataVisualization:
    def __init__(self):
        self.reservations = None
        self.screen = None

        self.height_multiplier = 1
        self.width_multiplier = 1

    def setup(self, reservations, head_line, show_invalid):
        self.reservations = reservations

        self.height_multiplier = reservations[0].height_multiplier

        self.create_window(1000 * self.width_multiplier, 10 * self.height_multiplier, head_line)
        self.draw_reservations(show_invalid)
        self.action_loop()

    def create_window(self, width, height, title):
        self.screen = pygame.display.set_mode((width, height))
        pygame.init()
        pygame.display.set_caption(title)

    def draw_reservations(self, show_invalid):
        x_coordinate = 0
        for reservation in self.reservations:
            #  if x_coordinate + reservation.length < 1000 * self.width_multiplier:
                y_coordinate = (reservation.begin - 8) * self.height_multiplier
                height = reservation.size * self.height_multiplier
                color = reservation.color

                if reservation.x == -1:
                    if not show_invalid:
                        continue
                    pygame.draw.rect(self.screen, color, (x_coordinate, y_coordinate, reservation.length, height), 0)
                    x_coordinate += reservation.length
                else:
                    pygame.draw.rect(self.screen, color, (reservation.x, y_coordinate, reservation.length, height), 0)
                    x_coordinate += reservation.length

        pygame.display.flip()

    def action_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
