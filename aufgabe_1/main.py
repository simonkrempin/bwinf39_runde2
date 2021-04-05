import time
import reservation as rsv
import data_visualization as dv
import data_optimization as do

time_range = 8, 18  # starting time and ending time of
available_space = 1000

file = open('example1.txt')
reservations = []
for i in range(int(file.readline())):
    reservations.append(rsv.Reservation(list(map(int, file.readline().split()))))

# data before slightest optimization
data_vis = dv.DataVisualization()
data_vis.setup(reservations, 'before optimization', True)

# data after optimization
print('---- optimization -----')
start_time = time.time()
do = do.DataOptimization(reservations, time_range)
optimized_reservations = do.optimize()
print("---- %s seconds ----" % round((time.time() - start_time), 3))
data_vis.setup(reservations, 'after optimization', False)
