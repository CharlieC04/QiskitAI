from qiskit import Aer, IBMQ, transpile
from qiskit.providers.ibmq import least_busy
import numpy as np
import pandas as pd


"""
INPUTS: a string that specifies the backend to select, and a QuantumCircuit,
    used for checking requirements for IBMQ

OUTPUTS: a backend to run QuantumCircuits with

"""
def select_backend(backend, qc):
    if backend.lower() == "ibmq":
        if IBMQ.active_account() == None:
            IBMQ.load_account()
        provider = IBMQ.get_provider(hub="ibm-q")
        available_backends = provider.backends(filters=lambda x: x.configuration().n_qubits >= len(qc.qubits) and \
            not x.configuration().selectedBackendulator and x.status().operational==True)

        if len(available_backends) == 0:
            raise Exception("No suitable quantum backend found")

        return least_busy(available_backends)
    else:
        return Aer.get_backend(backend)


def measureX(qc, qubit, classicalBit):
    qc.h(qubit)
    qc.measure(qubit, classicalBit)
    return qc

def measureY(qc, qubit, classicalBit):
    qc.sdg(qubit)
    qc.h(qubit)
    qc.measure(qubit, classicalBit)
    return qc


class TestExecutor:
    """
    INPUTS:
        - qc: QuantumCircuit to run the tests 
        - noOfExperiments: number of times the the qc will be run
        - noOfMeasurements: number of times the qc will be measured after each run
        - qubit0: the first qubit to compare
        - qubit1: the second qubit to comapre
        - classicalBit0: the bit where the first qubit will be measured in
        - classicalBit1: the bit where the second qubit will be measured in
        - basis: the basis of the measurement
        - backend: the backend used to run the tests


    OUTPUT: the data of the execution of the tests, meaning
        a tuple of two numpy arrays, one for each qubit.
        Each numpy array contains a list of probabilities (float between 0 and 1)
        that the qubit was measured in state |0> during one trial
        Each trial is measured as many times as noOfMeasurements specifies

    """
    def runTestAssertEqual(self,
                           qc,
                           noOfExperiments,
                           noOfMeasurements,
                           qubit0,
                           qubit1,
                           classicalBit0,
                           classicalBit1,
                           basis,
                           backend):

        selectedBackend = select_backend(backend, qc)


        if basis.lower() == "x":
            measureX(qc, qubit0, classicalBit0)
            measureX(qc, qubit1, classicalBit1)
        elif basis.lower() == "y":
            measureY(qc, qubit0, classicalBit0)
            measureY(qc, qubit1, classicalBit1)
        else:
            qc.measure(qubit0, classicalBit0)
            qc.measure(qubit1, classicalBit1)


        qc_trans = transpile(qc, backend=selectedBackend)


        trialProbas0 = np.empty(noOfExperiments)
        trialProbas1 = np.empty(noOfExperiments) 

        for trialIndex in range(noOfExperiments):
            result = selectedBackend.run(qc_trans, shots=noOfMeasurements).result()
            counts = result.get_counts()

            nb0s_qubit0 = 0
            nb0s_qubit1 = 0
            for elem in counts:
                if elem[::-1][classicalBit0] == '0': nb0s_qubit0 += counts[elem]
                if elem[::-1][classicalBit1] == '0': nb0s_qubit1 += counts[elem]


            trialProbas0[trialIndex] = nb0s_qubit0 / noOfMeasurements
            trialProbas1[trialIndex] = nb0s_qubit1 / noOfMeasurements

        return (trialProbas0, trialProbas1)



    """
    INPUTS: same as runTestAssertEqual except the first one, which is a
        list of QuantumCircuit instead of just one

    OUTPUT: a list of the results of runTestsAssertEqual for each test

    """
    def runTestsAssertEqual(self,
                            initialisedTests,
                            noOfExperiments,
                            noOfMeasurements,
                            qubit0,
                            qubit1,
                            classicalBit0,
                            classicalBit1,
                            basis,
                            backend):
        return [self.runTestAssertEqual(qc, noOfExperiments, noOfMeasurements, qubit0, qubit1, classicalBit0, classicalBit1, basis, backend)
                    for qc in initialisedTests]





    """
    INPUTS:
        - qc: QuantumCircuit to run the tests
        - noOfExperiments: number of times the the qc will be run
        - noOfMeasurements: number of times the qc will be measured after each run 
        - qubit0: the first qubit to compare
        - qubit1: the second qubit to comapre
        - classicalBit0: the bit where the first qubit will be measured in
        - classicalBit1: the bit where the second qubit will be measured in
        - basis: the basis of the measurement
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests,
            which is a list of statevectors (aka lists)
    """
    #Return for each test the recreated "statevector" of 2 bits
    def runTestAssertEntangled(self,
                               qc,
                               noOfExperiments,
                               noOfMeasurements,
                               qubit0,
                               qubit1,
                               classicalBit0,
                               classicalBit1,
                               basis,
                               backend):


        selectedBackend = select_backend(backend, qc)


        if basis.lower() == "x":
            measureX(qc, qubit0, classicalBit0)
            measureX(qc, qubit1, classicalBit1)
        elif basis.lower() == "y":
            measureY(qc, qubit0, classicalBit0)
            measureY(qc, qubit1, classicalBit1)
        else:
            qc.measure(qubit0, classicalBit0)
            qc.measure(qubit1, classicalBit1)

        q1=[]
        q2=[]
        job = execute(qc, selectedBackend, shots=noOfMeasurements, memory=True)
        memory = job.result().get_memory()
        qubitDict = dict.fromkeys(['qubit0','qubit1'])
        qubitDict = {'qubit0': qubit0,'qubit1':qubit1}
        # print("new dict", qubitDict)
        classicalQubitIndex = 1
        for i in range (noOfExperiments):
            for qubit in qubitDict.keys():
                # print("this qubit:",qubit)
                for measurement in memory:
                    # print("this measurement", measurement)
                    if (measurement[2-classicalQubitIndex] == '0'):
                        # print("measure: ",measurement[2-classicalQubitIndex],"also: qubittoassert0",qubitList[0],"and qubittoassert1: ",qubitList[1])    
                        if(qubit=='qubit0'):
                            q1.append(measurement[2-classicalQubitIndex])
                            # print("Added to q1 for measure0:", measurement[2-classicalQubitIndex])
                        else:
                            q2.append(measurement[2-classicalQubitIndex])
                            # print("Added to q2 for measure0:", measurement[2-classicalQubitIndex])
                    else:
                        # print("measureOTHER: ",measurement[2-classicalQubitIndex], "also: qubittoassert0",qubitList[0],"and qubittoassert1: ",qubitList[1]) 
                        if(qubit=='qubit0'):
                            q1.append(measurement[2-classicalQubitIndex])
                            # print("Added to q1 for measure1:", measurement[2-classicalQubitIndex])
                        else:
                            q2.append(measurement[2-classicalQubitIndex])    
                            # print("Added to q2 for measure1:", measurement[2-classicalQubitIndex])               
                classicalQubitIndex+=1

        measDict = dict.fromkeys(['qubit1','qubit2'])
        measDict = {'qubit1': q1,'qubit2':q2}
        measDf1 = pd.DataFrame.from_dict(measDict,orient='index')
        measDf12=measDf1.transpose()
        print(measDf12)
        # print(measDf12)
        ct = pd.crosstab(measDf12.qubit1,measDf12.qubit2)
        return ct



    """
    INPUTS:
        - qc: QuantumCircuit to run the tests
        - noOfExperiments: number of times the the qc will be run
        - noOfMeasurements: number of times the qc will be measured after each run
        - qubit0: the first qubit to compare
        - qubit1: the second qubit to comapre
        - classicalBit0: the bit where the first qubit will be measured in
        - classicalBit1: the bit where the second qubit will be measured in
        - basis: the basis of the measurement
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests,
            which is a list of lists of statevectors (aka lists)
    """
    def runTestsAssertEntangled(self,
                                initialisedTests,
                                noOfExperiments,
                                noOfMeasurements,
                                qubit0,
                                qubit1,
                                classicalBit0,
                                classicalBit1,
                                basis,
                                backend):
        return [self.runTestAssertEntangled(qc, noOfExperiments, noOfMeasurements, qubit0, qubit1, classicalBit0, classicalBit1, basis, backend)
                    for qc in initialisedTests]





    """
    INPUTS:
        - qc: QuantumCircuit to run the tests
        - noOfExperiments: number of times the the qc will be run
        - noOfMeasurements: number of times the qc will be measured after each run
        - qubit0: the first qubit to compare
        - measuredBit: the bit where the qubit will be measured in
        - basis: the basis of the measurement
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests,
            which is like runTestAssertEqual but without but for only one qubit instead of two
    """
    def runTestAssertProbability(self,
                                 qc,
                                 noOfExperiments,
                                 noOfMeasurements,
                                 qubit0,
                                 measuredBit,
                                 basis,
                                 backend):

        selectedBackend = select_backend(backend, qc)


        if basis.lower() == "x":
            measureX(qc, qubit0, measuredBit)
        elif basis.lower() == "y":
            measureY(qc, qubit0, measuredBit)
        else:
            qc.measure(qubit0, measuredBit)


        qc_trans = transpile(qc, backend=selectedBackend)


        trialProbas = np.empty(noOfExperiments)

        for trialIndex in range(noOfExperiments):
            result = selectedBackend.run(qc_trans, shots = noOfMeasurements).result()
            counts = result.get_counts()

            nb0s = 0
            for elem in counts:
                #Bit oredering is in the reverse order for get_count
                #(if we measure the last bit, it will get its value in index 0 of the string for some reason)
                if elem[::-1][measuredBit] == '0': nb0s += counts[elem]


            trialProba = nb0s / noOfMeasurements

            trialProbas[trialIndex] = trialProba

        return trialProbas


    """
    INPUTS:
        - initialisedTests: list of QuantumCircuits to run the tests
        - noOfExperiments: number of times the the qc will be run
        - noOfMeasurements: number of times the qc will be measured after each run
        - qubit0: the first qubit to compare
        - measuredBit: the bit where the qubit will be measured in
        - basis: the basis of the measurement
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests,
            which is like runTestsAssertEqual but without but for only one qubit instead of two
    """
    def runTestsAssertProbability(self,
                                  initialisedTests,
                                  noOfExperiments,
                                  noOfMeasurements,
                                  qubit0,
                                  measuredBit,
                                  basis,
                                  backend):
        return [self.runTestAssertProbability(qc, noOfExperiments, noOfMeasurements, qubit0, measuredBit, basis, backend)
                    for qc in initialisedTests]






    """
    INPUTS:
        - initialisedTests: list of QuantumCircuits to run the tests
        - noOfExperiments: number of times the the qc will be run
        - noOfMeasurements: number of times the qc will be measured after each run
        - qubit0: the first qubit to compare
        - measuredBit: the bit where the qubit will be measured in
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests,
            which is like runTestsAssertEqual but for 3 bases
    """
    def runTestsAssertState(self,
                            initialisedTests,
                            noOfExperiments,
                            noOfMeasurements,
                            qubit0,
                            measuredBit,
                            backend):
        tests_Y = [qc.copy() for qc in initialisedTests]
        tests_X = [qc.copy() for qc in initialisedTests]

        return (self.runTestsAssertProbability(initialisedTests, noOfExperiments, noOfMeasurements, qubit0, measuredBit, "z", backend),
                self.runTestsAssertProbability(tests_Y, noOfExperiments, noOfMeasurements, qubit0, measuredBit, "y", backend),
                self.runTestsAssertProbability(tests_X, noOfExperiments, noOfMeasurements, qubit0, measuredBit, "x", backend))




    """
    INPUTS:
        - qc: QuantumCircuit to run the tests
        - noOfMeasurements: number of measurements
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests
    """
    def runTestAssertMostProbable(self,
                                  qc,
                                  noOfMeasurements,
                                  backend):

        selectedBackend = select_backend(backend, qc)

        nbBits = len(qc.clbits)


        qc.measure_all()

        qc_trans = transpile(qc, backend=selectedBackend)

        result = selectedBackend.run(qc_trans, shots=noOfMeasurements).result()
        counts = result.get_counts()

        cut_counts = {}
        for key, value in counts.items():
            if key[:-(nbBits+1)] in counts:
                cut_counts[key[:-(nbBits+1)]] += value
            else:
                cut_counts[key[:-(nbBits+1)]] = value

        return sorted(cut_counts.items(), key=lambda x:x[1])


    """
    INPUTS:
        - initialisedTests: list of QuantumCircuits to run the tests
        - noOfMeasurements: number of measurements
        - backend: the backend used to run the tests


    OUTPUT:
        - the data of the execution of the tests
    """
    def runTestsAssertMostProbable(self,
                                   initialisedTests,
                                   noOfMeasurements,
                                   backend):
        return [self.runTestAssertMostProbable(qc, noOfMeasurements, backend) for qc in initialisedTests]


    # def runTestsAssertPhase(self,qc,noOfMeasurements,qubit0,qubit1,expectedPhases,classicalbit0,classicalbit1,noOfExperiments):
    #     selectedBackend = select_backend(backend, qc)
    #     qubitList = [qubit0,qubit1]
    #     for trialIndex in range(noOfExperiments):
    #         (x,y) = getDf(qc,qubitList,noOfMeasurements,selectedBackend)
    #         ## make a dataframe that contains p values of chi square tests to analyse results
    #         ## if x and y counts are both 25/25/25/25, it means that we cannot calculate a phase
    #         ## we assume that a qubit that is in |0> or |1> position to have 50% chance to fall 
    #         ## either way, like a coin toss: We treat X and Y results like coin tosses 
    #         pValues = pd.DataFrame(columns=['X','Y'])    
    #         pValues['X'] = resDf.apply(lambda row: applyChiSquareX(row, measurements_to_make/2), axis=1)
    #         pValues['Y'] = resDf.apply(lambda row: applyChiSquareY(row, measurements_to_make/2), axis=1)




    # def getDf(qc,qubitList,noOfMeasurements,selectedBackend):

    #     ## divide measurements to make by 3 as we need to run measurements twice, one for x and one for y
    #     ## divide measurements to make by 2 as we need to run measurements twice, one for x and one for y
    #     noOfMeasurements = noOfMeasurements // 2

    #     ## copy the circit and set measurement to y axis
    #     yQuantumCircuit = measureY(qc.copy(), qubitList)

    #     ## measure the x axis
    #     xQuantumCircuit = measureX(qc.copy(), qubitList)

    #     ## get y axis results
    #     yJob = execute(yQuantumCircuit, selectedBackend, shots=noOfMeasurements, memory=True)
    #     yCounts = yJob.result().get_counts()

    #     ## get x axis results
    #     xJob = execute(xQuantumCircuit, selectedBackend, shots=noOfMeasurements, memory=True)
    #     xCounts = xJob.result().get_counts()

    #     ## make a df to keep track of the predicted angles 
    #     resDf = pd.DataFrame(columns=['+','i','-','-i'])

    #     ## fill the df with the x and y results of each qubit that is being asserted
    #     classicalQubitIndex = 1
    #     for qubit in qubitList:
    #         plus_amount, i_amount, minus_amount, minus_i_amount = 0,0,0,0
    #         for experiment in xCounts:
    #             if (experiment[len(qubitList)-classicalQubitIndex] == '0'):
    #                 plus_amount += xCounts[experiment]
    #             else:
    #                 minus_amount += xCounts[experiment]
    #         for experiment in yCounts:
    #             if (experiment[len(qubitList)-classicalQubitIndex] == '0'):
    #                 i_amount += yCounts[experiment]
    #             else:
    #                 minus_i_amount += yCounts[experiment]
    #         df = {'+':plus_amount, 'i':i_amount,
    #             '-':minus_amount, '-i':minus_i_amount}
    #         resDf = resDf.append(df, ignore_index = True)
    #         classicalQubitIndex+=1

    #     ## convert the columns to a strict numerical type
    #     resDf['+'] = resDf['+'].astype(int)
    #     resDf['i'] = resDf['i'].astype(int)
    #     resDf['-'] = resDf['-'].astype(int)
    #     resDf['-i'] = resDf['-i'].astype(int)

    #     xAmount = resDf['-'].tolist()
    #     yAmount = resDf['-i'].tolist()  
    #     return (xAmount,yAmount)


