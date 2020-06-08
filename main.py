import sys
from math import sqrt
from tkinter import Tk, Canvas
from time import sleep
from ACS import ACS

f = open("n20w20.001.txt","r")
lines = f.readlines()
f.close()

def extractCrities(lines):
    vector = []
    for line in lines:
        data = line.replace("      ","\t").split("\t")
        vector.append((int(data[0].strip()),float(data[1].strip()), float(data[2].strip())))
    return vector

def costMatrix(cities):
    matrix=[]
    for i in range(0, len(cities)):
        matrix.append( [ sqrt( (cities[i][1]- cities[j][1])**2 + (cities[i][2]- cities[j][2])**2 ) for j in range (0, len(cities))] )
    return matrix


cities = extractCrities(lines[6:len(lines)-1]) #From 5 when 100, 6 when 20
costs = costMatrix(cities)
args = [
    0,
    10,
    2,
    0.9,
    0.1,
    0.1,
    1/(20*200)
]

""" root = Tk()
canvas = Canvas(root, width=600, height=600)
canvas.pack()
r = 7
scale =10
 """
#bests=[]

ACS = ACS(cities, costs, args)
print("***********************************")
print("Average cost: ", ACS.ave)
print("Current Best tour: ", end="")
print(ACS.currentBest.tour)
ACS.currentBest.printTour()
print("Current Best cost: ", ACS.currentBest.cost)
print("Current Optimum tour: ", end="")
ACS.globalOptimum.printTour()
print("Current Optimum cost: ", ACS.globalOptimum.cost)
#bests.append(ACS.globalOptimum)

for i in range(int(sys.argv[1])):
    ACS.run()
    print("***********************************")
    print("Iteration :", i)
    print("Average cost: ", ACS.ave)
    print("Current Best tour: ", end="")
    ACS.currentBest.printTour()
    print("Current Best cost: ", ACS.currentBest.cost)
    print("Current Optimum tour: ", end="")
    ACS.globalOptimum.printTour()
    print("Current Optimum cost: ", ACS.globalOptimum.cost)
"""     if bests[-1].cost > ACS.globalOptimum.cost:
        bests.append(ACS.globalOptimum)

for globalOptimum in bests:
    canvas.create_rectangle(0, 0, 600, 600, fill="white")
    for i in range(len(globalOptimum.tour) -1):
        canvas.create_line(scale*globalOptimum.tour[i][1],scale*globalOptimum.tour[i][2], scale*globalOptimum.tour[i+1][1], scale*globalOptimum.tour[i+1][2], width=3)
    for city in cities:
        canvas.create_oval(scale*city[1]-r, scale*city[2]-r,scale*city[1]+r,scale*city[2]+r, fill="blue")
    root.update_idletasks()
    root.update()
    sleep(1)

input("TO STOP PRESS ANYTHING") """