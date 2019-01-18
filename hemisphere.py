import math as m
import csv

r=0.25
hemisphere=[]
for j in range(0, 90, 2):
    alf = j*m.pi/180
    for i in range(0, 360, 2):
        fi = i*m.pi/180
        x = round(r * m.cos(alf) * m.cos(fi), 4)
        y = round(r * m.cos(alf) * m.sin(fi), 4)
        z = round(0.1 + r * m.sin(alf), 4)
        point=[x, y, z]
        hemisphere.append(point)

hemisphere.reverse()

print(hemisphere)
print(len(hemisphere))


FILENAME = "hemisphere.csv"
with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(hemisphere)
