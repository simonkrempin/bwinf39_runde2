import reservation as rsv
import data_visualization as dv

time_range = 8, 18  # starting time and ending time of
available_space = 1000
space = [[0 for i in range(available_space)] for j in range(time_range[1] - time_range[0])]

file = open('example4.txt')
rectangles = []
for i in range(int(file.readline())):
    rectangles.append(rsv.Reservation(list(map(int, file.readline().split()))))

data_vis = dv.DataVisualization(rectangles)
