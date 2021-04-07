class DataOptimization:
    def __init__(self, reservations, time_range):
        self.reservations = reservations
        self.height_multiplier = reservations[0].height_multiplier

        # creating a reservation cube which stores every reservation based on their begin and ending time
        self.duration = time_range[1] - time_range[0]
        self.time_range = time_range
        self.tensor = [[[] for j in range(self.duration)] for i in range(self.duration+1)]

    def optimize(self):
        self.reservations.sort(key=lambda x: x.size, reverse=True)  # sort reservations after size
        self.try_fit()
        self.show_space_used()

    def try_fit(self):
        for i in range(len(self.reservations)):
            interfering_reservations = self.get_reservation_from_tensor(self.reservations[i])
            interfering_reservations.sort(key=lambda element: element.x, reverse=False)  # sort the reservations after x position
            x_pos = self.find_first_valid_position(interfering_reservations, self.reservations[i])
            self.reservations[i].x = x_pos

            # only add the reservations which really fit inside the available space
            if x_pos >= 0:
                self.add_reservation_to_tensor(self.reservations[i])

    def add_reservation_to_tensor(self, r):
        x_value = r.ending - self.time_range[0]
        y_value = r.begin - self.time_range[0]
        self.tensor[x_value][y_value].append(r)

    def get_reservation_from_tensor(self, r):
        arr = []

        x_range = self.duration - (r.begin - self.time_range[0])
        x_start = r.begin - self.time_range[0] + 1
        # this must always start at 8 because of this example [8-15] and [9-10] 1 interferes with 2
        y_range = r.ending - self.time_range[0]

        for i in range(x_range):
            for j in range(y_range):
                for reservation in self.tensor[i + x_start][j]:
                    arr.append(reservation)

        return arr

    def find_first_valid_position(self, interfering_reservations, fitting_reservation):
        x_pos = 0
        for reservation in interfering_reservations:
            if reservation is interfering_reservations[-1]:
                if reservation.x + reservation.length + fitting_reservation.length > 1000:
                    if self.fit_rectangle_inside_last_space(fitting_reservation, reservation, x_pos + fitting_reservation.length) is True:
                        break
            if reservation.x - x_pos >= fitting_reservation.length:
                break
            x_pos = reservation.x + reservation.length

        if x_pos + fitting_reservation.length > 1000:
            return -1
        return x_pos

    def show_space_used(self):
        print('---- optimization -----')
        available_space = 1000 * 10
        used_space = 0
        for reservation in self.reservations:
            if reservation.x == -1:
                continue
            used_space += reservation.size * reservation.length
        print(f"available space : {available_space}\nused space      : {used_space}\nfree space      : {available_space - used_space}")

    # ----------------------------------
    # further optimizations
    # ----------------------------------

    def fit_rectangle_inside_last_space(self, fitting_reservation, after_reservation, new_x=0):
        interfering_reservations = self.get_reservation_from_tensor(after_reservation)
        after_interfering_reservations = [x for x in interfering_reservations if x.x > new_x]

        # if there is another reservation after can it be moved as well
        if len(after_interfering_reservations) == 1:
            if self.fit_rectangle_inside_last_space(after_reservation, after_interfering_reservations[0], new_x + after_reservation.length) \
                    and new_x + after_reservation.length <= 1000:
                after_reservation.x = new_x
                return True

        elif len(after_interfering_reservations) == 0:
            if new_x + after_reservation.length <= 1000:
                after_reservation.x = new_x
                return True
        return False
