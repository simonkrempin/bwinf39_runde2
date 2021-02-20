# reading the file
file = open("example1.txt")  # change the input file for the algorithm
circumference = int(file.readline().split()[0])
house_positions = list(map(int, file.readline().split()))
print(house_positions)

