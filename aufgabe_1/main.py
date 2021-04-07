import time
import reservation as rsv
import data_visualization as dv
import data_optimization as do

time_range = 8, 18  # starting time and ending time of
available_space = 1000

# get the input from the user
file = None
print('please enter a number for the example')
while True:
    user_input = input()
    try:
        try:
            user_input = int(user_input)
            file = open('example' + str(user_input) + '.txt')
        except ValueError:
            file = open(user_input)
        break
    except FileNotFoundError:
        print('please enter a valid input')

# read the data form the file
reservations = []
for i in range(int(file.readline())):  # only takes reservations based on the first value inside the text file
    reservations.append(rsv.Reservation(list(map(int, file.readline().split())), i+1))

# data before slightest optimization
data_vis = dv.DataVisualization()
data_vis.setup(reservations, 'before optimization', True)

# data after optimization
start_time = time.time()
do = do.DataOptimization(reservations, time_range)
optimized_reservations = do.optimize()
print("---- %s seconds ----" % round((time.time() - start_time), 3))

# write the fitting reservations inside a text file as a final result
f = open('solution.txt', 'w')
reservations.sort(key=lambda element: element.index, reverse=False)  # sort the reservations after index
for reservation in reservations:
    f.write(f'reservation ' + str(reservation.index) + ' got picked and goes from ' + str(reservation.x) + ' to ' +
            str(reservation.x + reservation.length) + '\n') if reservation.x != -1 else ''
f.close()

data_vis.setup(reservations, 'after optimization', False)
