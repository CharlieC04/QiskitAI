from qiskit import transpile

class CostFunction:

    def __init__(self, problemType, problem):
        self.problemType = problemType
        self.problem = problem

    def getCost(self, value):
        if ('maxcut' in self.problemType):
            return self.__getCostMaxcut(value)
        
        elif ('3SAT' in self.problemType):
            return self.__getCost3SAT(value)
        
        return 0
    
    
    
    def getExpectation(self, counts):
        avg = 0
        sum_count = 0
        for bit_string, count in counts.items():
            obj = self.getCost(bit_string)
            avg += obj * count
            sum_count += count
        return avg/sum_count
    
    def getBestExpectation(self, counts, goal, randomGuess, shots):
        count = 0
        minScore = self.getCost(min(counts.keys(), key=lambda x: self.getCost(x)))
        for key, value in counts.items():
            if (self.getCost(key) == minScore):
                count += value

        if (minScore != goal):
            count = 0
        return minScore, (count / (shots))
    
    def getMostCommonExpectation(self, counts):
        return self.getCost(max(counts, key=counts.get))

    
    def getDesiredExpectation(self, counts, shots=1000):

        minScore = self.getCost(min(counts.keys(), key=lambda x: self.getCost(x)))
        score = minScore * shots

        for key, value in counts.items():
            if (self.getCost(key) == minScore):
                score -= value
        
        return score

 


    def __getCostMaxcut(self, partition):
        score = 0

        part = partition[::-1]
    
        for edge in self.problem.edges():
            v1 = edge[0]
            v2 = edge[1]
            if part[v1] != part[v2]:
                score-=1

        return score
    
    def __getCost3SAT(self, partition):
        score = 0
    
        if (partition == "0010" or partition == "0100"):
            score -= 1

        

        return score
