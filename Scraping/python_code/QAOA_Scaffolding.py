import networkx as nx
import sys
sys.path.append(
    "/Users/johnburke/Desktop/QAOA Code/")

from qiskit import Aer, transpile
from scipy.optimize import minimize
from QAOA_Circuit import QAOACircuit
from QAOA_Cost_Function import CostFunction
import numpy as np

class Result:

    def __init__(self, fun, x, nfev):
        self.fun = fun
        self.x = x
        self.nfev = nfev

    def addHistory(self, history):
        self.history = history

class QAOAScaffolding:
    circuit = None
    simulator = None
    built = False

    def __init__(self, numQubits, problemType, problem):
        self.numQubits = numQubits
        self.problemType = problemType
        self.problem = problem

    def build(self, layers, mixerType, initType, shots):
        qc = QAOACircuit(self.numQubits, layers, mixerType, self.problem, self.problemType, initType)
        qc.build()
        self.layers = layers
        self.circuit = qc
        self.simulator = Aer.get_backend('qasm_simulator')
        self.shots = shots

        # if ('maxcut' in self.problemType):
        cost = CostFunction(self.problemType, self.problem)
        self.costFunction = cost

        self.built = True

    def getExpectation(self, params, method = 'average_expectation', customSimulator= None, goal=0, randomGuess=None):
        if (customSimulator):

            counts = customSimulator(params, self.shots)
        else:

            qc = self.circuit.getCircuitWithParameters(params)

        
            
            qc = transpile(qc, backend=self.simulator)
            counts = self.simulator.run(qc, shots=self.shots).result().get_counts()
        if method == 'best_expectation':
            return self.costFunction.getBestExpectation(counts, goal, randomGuess, self.shots)
        elif method == "most_common_expectation":
            return self.costFunction.getMostCommonExpectation(counts)
        elif method == "desired_expectation":
            return self.costFunction.getDesiredExpectation(counts, self.shots)
        # elif method == "count_of_best":
        #     return self.costFunction.getDesiredExpectation(counts, self.shots)
        

        return self.costFunction.getExpectation(counts)
    
    
    def minimizeExectation(self, initialParamsType = 'constant', minimizerType = 'scipy', customParameters = [], saveHistory = False, measurementStrategy = "average_expectation", customSimulator = None, goal=0, graph=None, guess=1):
         if (not self.built):
             print("Circuit not built")
             return False
         
         initialParams = []
         parameterCount = self.circuit.getNumberOfParameters()
         if (initialParamsType == 'constant'):
             initialParams = [1.0] * parameterCount
             

         elif (initialParamsType =='random'):
             initialParams = np.random.uniform(0.0, np.pi, parameterCount)

         elif (initialParamsType == 'custom'):
             initialParams = customParameters

         if (minimizerType == 'scipy'):
             return self.__scipyMinimize(initialParams, measurementStrategy, customSimulator=customSimulator)
         elif (minimizerType == 'brute_force'):
             return self.__bruteForceMinimize(parameterCount, saveHistory, measurementStrategy)
         elif (minimizerType == 'brute_force_custom'):
             return self.__bruteForceCustom(parameterCount, saveHistory, measurementStrategy, customSimulator=customSimulator)
         elif (minimizerType == 'annealing'):
             return self.__annealingMinimize(initialParams, 1000, 1, saveHistory, measurementStrategy)
         elif (minimizerType == 'z_custom'):
             return self.__bruteForceZCustom(parameterCount ,saveHistory)
         elif (minimizerType == 'y_custom_1'):
             return self.__bruteForceYCustom1(parameterCount ,saveHistory)
         elif (minimizerType == 'y_custom_2'):
             return self.__bruteForceYCustom2(parameterCount, measurementStrategy,saveHistory)
         elif (minimizerType == 'y_custom_3'):
             return self.__bruteForceYCustom3(parameterCount, saveHistory, graph=graph)
         elif (minimizerType == 'ma_rz_custom'):
             return self.__customMARZOptimizer(parameterCount, saveHistory, graph=graph, guess=guess)
         elif (minimizerType == 'ma_rz_custom_2'):
             return self.__customMARZOptimizer2(parameterCount, saveHistory, graph=graph, guess=guess)
         elif (minimizerType == 'ry_custom'):
             return self.__customCXRYOptimizer(parameterCount, saveHistory, graph=graph)
        
         
    
    def __scipyMinimize(self, initialParams, measurementStrategy = 'average_expectation', customSimulator=None):
        res = minimize(self.getExpectation,
            initialParams,
            args=(measurementStrategy, customSimulator),
            method='COBYLA',
            options={'maxiter':1000})
        
        return res
    
    def __bruteForceMinimize(self, parameterCount, saveHistory = False, measurementStrategy = 'average_expectation'):
        possibleValues = 100
        values = np.linspace(0, 2*np.pi, possibleValues, endpoint=False)
        bestExpectation = 0
        bestParameters = []
        allValues = []
        
        for i in range(0, possibleValues ** parameterCount):
            parameters = [values[int(i / (possibleValues ** j)) % possibleValues] for j in range(0, parameterCount)]
            expectation = self.getExpectation(parameters, measurementStrategy)

            if (saveHistory):
                allValues.append((parameters, expectation))
            
            if (expectation < bestExpectation):
                bestExpectation = expectation
                bestParameters = parameters

        res = Result(bestExpectation, bestParameters, possibleValues ** parameterCount)

        if (saveHistory):
            res.addHistory(allValues)

        return res
    
    def __annealingMinimize(self, initialParams, temp, stepSize, saveHistory = False, measurementStrategy = 'average_expectation'):

        def temp_reduction(temp, alpha, type='linear', beta=1):
            if (type == 'linear'):
                return temp - alpha
            if (type == 'geometric'):
                return temp * alpha
            if (type == 'slow'):
                return (temp / (1 + beta * alpha))
        
        def perturb_params(params, curr_temp, max_temp):
            new_params = params.copy()
            max_terms_changed = int((curr_temp / max_temp)) * len(new_params)
            
            if (max_terms_changed <= 0):
                max_terms_changed = 1
                states_changed = max_terms_changed
            else:
                states_changed = np.random.randint(1, max_terms_changed)
            scale = (curr_temp / max_temp) * np.pi
            
            for i in range(states_changed):
                index = np.random.randint(0, len(new_params))
                new_params[index] = new_params[index] + np.random.uniform(-scale , scale)
            return np.array(new_params) % (np.pi / 2)
        
        curr_cost = self.getExpectation(initialParams, measurementStrategy)
        curr_temp = temp
        curr_params = initialParams
        niter = 0
        allValues = []
        while curr_temp > 1:
            niter += 1
            curr_temp = temp_reduction(curr_temp, stepSize)
            new_params = perturb_params(curr_params, curr_temp, temp)
            new_cost = self.getExpectation(new_params, measurementStrategy)

            if (saveHistory):
                allValues.append((new_params, new_cost))
            if (new_cost < curr_cost):
                curr_cost = new_cost
                curr_params = new_params
            else:
                cost_dif = (curr_cost - new_cost) * 1000
                prob = np.e ** (cost_dif / curr_temp)
                if (np.random.random() <= prob):
                    curr_cost = new_cost
                    curr_params = new_params

        res = Result(curr_cost, curr_params, niter)
        if (saveHistory):
            res.addHistory(allValues)

        return res
    

    def __bruteForceCustom(self, parameterCount, saveHistory = False, measurementStrategy = 'average_expectation', customSimulator=None):
        possibleParams = [0.0, np.pi/2, np.pi]
        bestExpectation = 0.0
        parameters = [0.0] * parameterCount
        
        for i in range(0, parameterCount):
            testParams = parameters
            for param in possibleParams:
                testParams[i] = param
                expectation = self.getExpectation(testParams, measurementStrategy, customSimulator)
                print(expectation, testParams)
                if (expectation < bestExpectation):
                    bestExpectation = expectation
                    parameters[i] = param


    def __bruteForceZCustom(self, parameterCount, saveHistory = False, customSimulator=None):
        possibleParams = [0.0, np.pi/2, 2*np.pi/2, 3*np.pi/2]
        parameters = [0.0] * parameterCount
        bestCost = 0.0
        
        for param1 in possibleParams:
            for param2 in possibleParams:
                for param3 in possibleParams:
                    params = [param1, param2, param3]
                    newCost = self.getExpectation(params, "desired_expectation")
                    if (newCost < bestCost):
                        parameters = params
                        bestCost = newCost
            


        res = Result(bestCost, parameters, 16)


        return res
    
    def __bruteForceYCustom1(self, parameterCount, saveHistory = False, customSimulator=None):
        
        parameters = [0.0] * parameterCount
        bestCost = 0.0

        for i in range(0, parameterCount):
            exp1 = self.getExpectation(parameters, "average_expectation")
            parameters[i] = np.pi/2
            exp2 = self.getExpectation(parameters, "average_expectation")
            bestCost = exp2

            if (exp1 < exp2):
                parameters[i] = 0
                bestCost = exp1

        res = Result(bestCost, parameters, parameterCount)


        return res
    
    def __bruteForceYCustom2(self, parameterCount, measurementStrategy = 'average_expectation', saveHistory = False, customSimulator=None):

        theta = np.pi/4
        
        parameters = [theta] * parameterCount
        bestCost = 0.0

        # parameters[0] = np.pi/2

        # parameters[1] = np.pi/2

        # parameters[2] = np.pi/2
        # parameters[3] = 0
        # parameters[4] = 0

        # parameters[5] = np.pi/2
        # parameters[6] = 0
        # parameters[7] = 0

        # parameters[8] = np.pi/2
        # parameters[9] = 0
        # parameters[10] = 0

        # parameters[11] = np.pi/2
        # parameters[12] = 0
        # parameters[13] = 0
        # parameters[14] = 0

        # parameters[15] = np.pi/2
        # parameters[16] = 0
        # parameters[17] = 0


        bestCost = self.getExpectation(parameters, measurementStrategy)
        iterations = 0

        
        # allWorse = False
        # while not allWorse:
            
        #     currBestCost = 0
        #     currBestI = -1
        #     bestChange = 0
        #     for i in range(0, parameterCount):
        #         if (parameters[i] == theta):
        #             iterations += 1
        #             parameters[i] = 0
        #             exp = self.getExpectation(parameters, measurementStrategy)
        #             if (exp < currBestCost):
        #                 currBestCost = exp
        #                 currBestI = i
        #                 bestChange = 0
        #             parameters[i] = np.pi/2
        #             exp = self.getExpectation(parameters, measurementStrategy)
        #             if (exp < currBestCost):
        #                 currBestCost = exp
        #                 currBestI = i
        #                 bestChange = np.pi/2
        #             # parameters[i] = np.pi/4
        #             # exp = self.getExpectation(parameters, measurementStrategy)
        #             # if (exp < currBestCost):
        #             #     currBestCost = exp
        #             #     currBestI = i
        #             #     bestChange = np.pi/4
        #             parameters[i] = theta
        #     if (currBestCost < bestCost):
        #         parameters[currBestI] = bestChange
        #         bestCost = currBestCost
        #     else:
        #         allWorse = True

        # for i in range(0, parameterCount):
        #     if (parameters[i] == theta):
        #         parameters[i] = 0
        #         exp = self.getExpectation(parameters, measurementStrategy)
        #         if (exp < bestCost):
        #             bestCost = exp
        #         else:
        #             parameters[i] = theta

        # for i in range(0, parameterCount):
        #     if (parameters[i] == theta):
        #         parameters[i] = np.pi/2
        #         exp = self.getExpectation(parameters, measurementStrategy)
        #         if (exp < bestCost):
        #             bestCost = exp
        #         else:
        #             parameters[i] = theta

        # bestCost = self.getExpectation(parameters, measurementStrategy)
                
            


        res = Result(bestCost, parameters, iterations)


        return res
    
    def __bruteForceYCustom3(self, parameterCount, saveHistory = False, customSimulator=None, graph=None):

        edges = list(graph.edges())
        v = len(graph.nodes)
        orderedEdges = []
        rightEdges = []

        j = list(range(1, v))

        for e in edges:
            e1 = e[0]
            e2 = e[1]
            if (e1 > e2):
                rightEdges.append((e2, e1))
            else:
                rightEdges.append(e)

       

        for e in rightEdges.copy():
            # print(e)
            e1 = e[0]
            e2 = e[1]
            if (e2 in j):
                rightEdges.remove(e)
                orderedEdges.append(e)
                j.remove(e2)

        
        
        bestCost = 0.0
        v = len(orderedEdges)

        parameters = [np.pi/2] * v + [0.0] * (parameterCount - v)

        bestCost = self.getExpectation(parameters, "average_expectation")
        allWorse = False

        while not allWorse:
            
            currBestCost = 0
            currBestI = -1
            for i in range(0, parameterCount):
                if (parameters[i] != np.pi/2):
                    parameters[i] = np.pi/2
                    exp = self.getExpectation(parameters, "average_expectation")
                    if (exp < currBestCost):
                        currBestCost = exp
                        currBestI = i
                    parameters[i] = 0.0
                else:
                    parameters[i] = 0
                    exp = self.getExpectation(parameters, "average_expectation")
                    if (exp < currBestCost):
                        currBestCost = exp
                        currBestI = i
                    parameters[i] = np.pi/2

            if (currBestCost < bestCost):
                if (parameters[currBestI] == np.pi/2):
                    parameters[currBestI] = 0
                else:
                    parameters[currBestI] = np.pi/2
                bestCost = currBestCost
            else:
                allWorse = True
            


        res = Result(bestCost, parameters, parameterCount)


        return res
    

    def __customMARZOptimizer(self, parameterCount, saveHistory = False, customSimulator=None, graph=None, guess=1):

        edges = list(graph.edges())
        v = len(graph.nodes)

        parameters = [np.pi/guess] * len(edges) + [np.pi/4]

        bestCost = self.getExpectation(parameters, "average_expectation")
        

        for i in range(0, len(edges)):
            parametersCopy = parameters.copy()
            parametersCopy[i] = 0.0
            cost = self.getExpectation(parametersCopy, "average_expectation")
            if (cost < bestCost):
                parameters = parametersCopy
                bestCost = cost

       
            


        res = Result(bestCost, parameters, len(edges))


        return res
    
    def __customMARZOptimizer2(self, parameterCount, saveHistory = False, customSimulator=None, graph=None, guess=1):

        edges = list(graph.edges())
        v = len(graph.nodes)

        parameters = [np.pi/6] + [np.pi/4]

        bestCost = self.getExpectation(parameters, "average_expectation")
        

        # for i in range(1, v+1):
        #     parametersCopy = parameters.copy()
        #     parametersCopy[i] = 0.0
        #     cost = self.getExpectation(parametersCopy, "average_expectation")
        #     if (cost < bestCost):
        #         parameters = parametersCopy
        #         bestCost = cost
        #     parametersCopy[i] = np.pi/2
        #     cost = self.getExpectation(parametersCopy, "average_expectation")
        #     if (cost < bestCost):
        #         parameters = parametersCopy
        #         bestCost = cost

       
            


        res = Result(bestCost, parameters, len(edges))


    def __customCXRYOptimizer(self, parameterCount, saveHistory = False, customSimulator=None, graph=None):

        edges = list(graph.edges())
        v = len(graph.nodes)

        initialCut = int(len(edges) / 2)

        parameters = [np.pi/(initialCut/2)]

        bestCost = self.getExpectation(parameters, "average_expectation")
        cutL = initialCut

        for i in range(1, 20):
            parametersCopy = [np.pi/(i/2)]
            cost = self.getExpectation(parametersCopy, "average_expectation")
            print(i, cost)
            if (cost < bestCost):
                parameters = parametersCopy
                bestCost = cost 
                cutL = i
            


        res = Result(bestCost, cutL, len(edges))


        return res



    
    




    
    
   


    

