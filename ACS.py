from random import randint, random

class ACS:
    def __init__(self, cities, costMatrix, args):
        self.nAnts = args[1]
        self.start = args[0]
        self.beta = args[2]
        self.q0 = args[3]
        self.alpha = args[4]
        self.rho = args[5]
        self.t0 = args[6]
        self.cities= cities
        self.currentBest = None
        self.globalOptimum = None
        self.ave=0
        self.cAndPMatrix, self.ants = self.initPhase(costMatrix, self.nAnts)
        self.run()
    
    def initPhase(self, matrix, nAnts):
        cAndP=[]
        for i in range(len(self.cities)):
            cAndP.append( [[matrix[i][j], self.t0] for j in range(len(self.cities)) ] )
        
        ants = []
        if self.start is not None:
            for i in range(nAnts):
                toVisit = self.cities[:self.start]
                toVisit.extend(self.cities[self.start+1:])
                ants.append(Ant(self.cities[self.start],toVisit))
        else:
            for i in range(nAnts):
                start = randint(0, len(self.cities)-1)
                toVisit = self.cities[:start]
                toVisit.extend(self.cities[start+1:])
                ants.append(Ant(self.cities[start],toVisit))
        
        return cAndP, ants

    def restartAnts(self):
        if self.start is not None:
            for i in range(len(self.ants)):
                toVisit = self.cities[:self.start]
                toVisit.extend(self.cities[self.start+1:])
                self.ants[i].restart(self.cities[self.start],toVisit)
        else:
            for i in range(len(self.ants)):
                start = randint(0, len(self.cities)-1)
                toVisit = self.cities[:start]
                toVisit.extend(self.cities[start+1:])
                self.ants[i].restart(self.cities[start],toVisit)
    
    def generateTours(self):
        for i in range(len(self.cities)-1):
            for ant in self.ants:
                nextCity = self.selectNextCity(ant.tour[i],ant.toVisit)
                ant.addToTour(nextCity)
                ant.visitCity(nextCity)
    
    def globalUpdate(self, best):
        tour = self.getTourEdges(best)
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                edge = "("+str(i)+","+str(j)+")"
                if tour.find(edge) != -1:
                    self.cAndPMatrix[i][j][1] = (1-self.alpha)*self.cAndPMatrix[i][j][1] + self.alpha/best.cost
                else:
                    self.cAndPMatrix[i][j][1] = (1-self.alpha)*self.cAndPMatrix[i][j][1]

    def getTourEdges(self, ant):
        edges = ""
        for city in range(len(ant.tour)):
            if city == len(ant.tour) -1:
                edges+="("+str(ant.tour[city][0]-1)+","+str(ant.start[0]-1)+")"
            else:
                edges+="("+str(ant.tour[city][0]-1)+","+str(ant.tour[city+1][0]-1)+")-"
        return edges

    def localUpdate(self, ant):
        for city in range(len(ant.tour)):
            if city == len(ant.tour) -1 :
                self.cAndPMatrix[ant.tour[city][0]-1][ant.start[0]-1][1] = (1-self.rho)*self.cAndPMatrix[ant.tour[city][0]-1][ant.start[0]-1][1]+self.rho*self.t0
            else:
                self.cAndPMatrix[ant.tour[city][0]-1][ant.tour[city+1][0]-1][1] = (1-self.rho)*self.cAndPMatrix[ant.tour[city][0]-1][ant.tour[city+1][0]-1][1]+self.rho*self.t0
    
    def calcTourCost(self, ant):
        cost = 0
        for city in range(len(ant.tour)):
            if city == len(ant.tour) -1 :
                cost+= self.cAndPMatrix[ant.tour[city][0]-1][ant.start[0]-1][0]
            else:
                cost+= self.cAndPMatrix[ant.tour[city][0]-1][ant.tour[city+1][0]-1][0]
        return cost

    def findBest(self):
        best = None
        ave =0
        for i in range(len(self.ants)):
            self.ants[i].cost = self.calcTourCost(self.ants[i])
            ave+=self.ants[i].cost/self.nAnts
            if best is None:
                best = self.ants[i]
            elif best.cost > self.ants[i].cost:
                best = self.ants[i]
        return best, ave

    def selectNextCity(self, actualCity, toVisit):
        best = None
        sumValues = 0
        probs = []
        for city in toVisit:
            value = self.cAndPMatrix[actualCity[0]-1][city[0]-1][1]*(1/self.cAndPMatrix[actualCity[0]-1][city[0]-1][0])**self.beta
            sumValues+=value
            if best is None:
                best = [city, value]
            elif best[1] < value:
                best = [city, value]
            probs.append([city, value])
        if random() <= self.q0 :
            return best[0]
        else:
            for i in range(len(probs)):
                probs[i][1] = probs[i][1]/sumValues
            probs.sort(key=lambda e: e[1])
            probExtraction = random()
            i = 0
            sumP = probs[0][1]
            while i<len(probs)-1 and sumP< probExtraction:
                i+=1
                sumP+=probs[i][1]
            return probs[i][0]
    
    def run(self):
        self.generateTours()
        for ant in self.ants :
            self.localUpdate(ant)
        self.currentBest, self.ave = self.findBest()
        self.currentBest = self.currentBest.copy()
        self.globalUpdate(self.currentBest)
        if self.globalOptimum is None:
            self.globalOptimum = self.currentBest
        elif self.globalOptimum.cost > self.currentBest.cost:
            self.globalOptimum = self.currentBest
        self.restartAnts()
        


class Ant:
    def __init__(self, start, toVisit):
        self.start = start
        self.toVisit = toVisit
        self.tour = [start]
        self.cost = None
    
    def visitCity(self, city):
        self.toVisit.remove(city)
    
    def addToTour(self, city):
        self.tour.append(city)
    
    def restart(self, start, toVisit):
        self.cost = None
        self.start = start
        self.tour = [start]
        self.toVisit = toVisit
    
    def copy(self):
        a = Ant(None, None)
        a.start = self.start[:]
        a.tour = self.tour[:]
        a.toVisit = self.toVisit[:]
        a.cost = self.cost
        return a
    
    def printTour(self):
        for city in range(len(self.tour)):
            if city != len(self.tour)-1:
                print(self.tour[city][0],"- ", end="")
            else:
                print(self.tour[city][0])