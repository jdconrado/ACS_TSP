import sys
from math import sqrt
from ACS import ACS

f = open("n20w20.002.txt","r")
lines = f.readlines()
f.close()

def extractCrities(lines):
    vector = []
    for line in lines:
        data = line.replace("      ","\t").replace("   ","\t").split("\t")
        vector.append((int(data[1]),float(data[2]), float(data[3])))
    return vector

def costMatrix(cities):
    matrix=[]
    for i in range(0, len(cities)):
        matrix.append( [ sqrt( (cities[i][1]- cities[j][1])**2 + (cities[i][2]- cities[j][2])**2 ) for j in range (0, len(cities))] )
    return matrix


cities = extractCrities(lines[6:len(lines)-1])
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

ACS = ACS(cities, costs, args)
print("***********************************")
print("Average cost: ", ACS.ave)
print("Current Best tour: ", end="")
ACS.currentBest.printTour()
print("Current Best cost: ", ACS.currentBest.cost)
print("Current Optimum tour: ", end="")
ACS.globalOptimum.printTour()
print("Current Optimum cost: ", ACS.globalOptimum.cost)

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