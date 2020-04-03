class Ant:
    def __init__(self,noOfCities):
        self.__noOfCities=noOfCities
        self.__repres=[]
        for i in range(self.__noOfCities):
            self.__repres.append(0)
        self.__visited=[]

    @property
    def repres(self):
        return self.__repres[:]

    def visitCity(self,currentIndex, city):
        self.__repres[currentIndex+1]=city
        self.__visited[city]=True

    def visited(self,cityIndex):
        if self.__visited[cityIndex]==True:
            return True
        return False

    def traiLength(self,matrix):
        length=0
        for i in range(0,len(self.__repres)-1):
            length+=matrix[self.__repres[i]][self.__repres[i+1]]
        length+=matrix[self.__repres[-1]][self.__repres[0]]
        return length

    def clear(self):
        self.__visited.clear()
        for i in range(0,self.__noOfCities):
            self.__visited.append(False)


