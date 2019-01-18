import csv
from d_genetic import *
from Genetic_end import *
import time

t = time.time()
n=0


new_list = []
q, result= evolution(4, [0, 0, 0.35])
FILENAME = "hemisphere.py"
FILENAME1 = "Genetic_result.csv"

with open(FILENAME, "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        coord = list(map(float, row))

        with open(FILENAME1, "a", newline="") as file:


            q, result = d_evolution(4, coord, q)


            if result > 0.01:
                q, result = evolution(4, coord)

            n += 1
            print(n, result, round(time.time()-t,1))

            new_line = coord+q

            writer = csv.writer(file)
            writer.writerow(new_line)



print('Process time:', time.time()-t, 'sec')
