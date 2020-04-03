from Ant import Ant
from random import randint, uniform

class AntColonyOptimization:
    def __init__(self,matrix, acoParam=None,problParam=None):
        self.__acoParam=acoParam
        self.__problParam=problParam
        self.__matrix=matrix
        self.__antPopulation=[]
        self.__noOfAnts=round(problParam['noOfCities']*acoParam['antFactor'])
        self.__probabilities=[]
        self.__currentIndex=0
        self.__trails=[]
        self.__bestRepres=[]
        self.__bestDistance=9999999999999

        self.__init_ants()
        # alpha=1 #importanta umrei=cate furnici au mai trecut pe muchia respectiv
        # beta=5 #importanta vizibilitatii=cat de aproape de urmatorul oras
        # evaporation=0.5
        # Q=500 #cantitate de feromon lasata de o furnica
        # antFactor=0.8
        # randomFactor=0.01

    @property
    def population(self):
        return self.__population


    def __init_ants(self):
        for i in range(self.__noOfAnts):
            self.__antPopulation.append(Ant(self.__problParam['noOfCities']))

    def __set_up_probabilities(self):
        for i in range(self.__problParam['noOfCities']):
            self.__probabilities.append(0.0)

    def __set_up_trails(self):
        for i in range(self.__problParam['noOfCities']):
            self.__trails.append([])
            for j in range(self.__problParam['noOfCities']):
                self.__trails[i].append(self.__acoParam['c'])

    def __nextGeneration(self):
        self.__currentIndex=0
        for i in range(self.__noOfAnts):
            self.__antPopulation[i].clear()
            city=randint(0,self.__problParam['noOfCities']-1)
            self.__antPopulation[i].visitCity(-1,city)

    def __calculateProbabilities(self, ant):
        currentCity=ant.repres[self.__currentIndex]
        feromon=0.0
        n=self.__problParam['noOfCities']
        for city in range(n):
            if not ant.visited(city):
                feromon+=((self.__trails[currentCity][city])**self.__acoParam['alpha'])*((1.0/self.__matrix[currentCity][city])**self.__acoParam['beta'])
        for oras in range(n):
            if ant.visited(oras):
                self.__probabilities[oras]=0.0
            else:
                nr=((self.__trails[currentCity][oras])**self.__acoParam['alpha'])*((1.0/self.__matrix[currentCity][oras])**self.__acoParam['beta'])
                self.__probabilities[oras]=nr/feromon

    def __selectNextCity(self, ant):
        #verificam daca putem face mutatie
        nr=uniform(0,1)
        if nr <self.__acoParam['randomFactor']:
            city=randint(0,self.__problParam['noOfCities']-self.__currentIndex-1)
            if not ant.visited(city):
                return city

        #probabilitati pt ant
        self.__calculateProbabilities(ant)
        total=0.0
        n = self.__problParam['noOfCities']
        for i in range(n):
            total+=self.__probabilities[i]
            if total>=nr:
                return i

    def __moveAnts(self):
        n=self.__problParam['noOfCities']-1
        for i in range(n):
            for ant in self.__antPopulation:
                city=self.__selectNextCity(ant)
                ant.visitCity(self.__currentIndex,city)
            self.__currentIndex+=1

    def __updateTrails(self):
        n = self.__problParam['noOfCities']
        for i in range(n):
            for j in range(n):
                self.__trails[i][j]*=self.__acoParam['evaporation']
        for ant in self.__antPopulation:
            contributie=self.__acoParam['Q']/ant.traiLength(self.__matrix)
            for k in range(n-1):
                self.__trails[ant.repres[k]][ant.repres[k+1]]+=contributie
            self.__trails[ant.repres[-1]][ant.repres[0]]+=contributie

    def solve(self):
        self.__set_up_probabilities()
        self.__set_up_trails()
        n=self.__problParam['maxIterations']
        for i in range(n):
            self.__nextGeneration()
            self.__moveAnts()
            self.__updateTrails()
            for ant in self.__antPopulation:
                antDistance=ant.traiLength(self.__matrix)
                if antDistance<self.__bestDistance:
                    self.__bestDistance=antDistance
                    self.__bestRepres=ant.repres
            print("Generation "+str(i)+" Best repres.: "+str(self.__bestRepres)+" dist="+str(self.__bestDistance))