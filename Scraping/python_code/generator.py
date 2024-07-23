from qiskit import QuantumCircuit
from TestProperty import TestProperty
import cmath
import numpy as np
from math import cos, sin, radians, degrees
import random

class Generator:
    """
    This method generates one concrete test case and provides the exact parameters
        used to initialise the qubits

    Inputs: a TestProperty

    Output: a tuple containing the initialised test (a QantumCircuit),
        and two dictionaries, that store the theta (first one) and phi (second one)
        of each qubit in degrees

    """
    def generateTest(self, testProperties: TestProperty):

        preConditions = testProperties.preConditions
        phiVal = {}
        thetaVal = {}

        #Adds 2 classical bits to read the results of any assertion
        #Those bits will not interfere with the normal functioning of the program
        if testProperties.minQubits == testProperties.maxQubits:
            noOfQubits = testProperties.minQubits
        else:
            noOfQubits = np.random.randint(testProperties.minQubits, testProperties.maxQubits)

        qc = QuantumCircuit(noOfQubits, testProperties.noOfClassicalBits + 2)

        for key, value in preConditions.items():
            #ignores the keys that are outside of the range
            if key >= noOfQubits:
                continue

            #converts from degrees to radian
            randPhi = random.randint(value.minPhi, value.maxPhi)
            randTheta = random.randint(value.minTheta, value.maxTheta)

            #stores the random values generated
            phiVal[key] = randPhi
            thetaVal[key] = randTheta

            randPhiRad = radians(randPhi)
            randThetaRad = radians(randTheta)

            """WHY THIS HAPPEN"""
            value0 = cos(randThetaRad/2)
            value1 = cmath.exp(randPhiRad * 1j) * sin(randThetaRad / 2)

            qc.initialize([value0, value1], key)

        return (qc, thetaVal, phiVal)



    """
    This method runs self.generateTest to generate the specified amount of tests in
        the TestProperty

    Inputs: a TestProperty

    Outputs: a list of what self.generateTests returns (a tuple containing a QuantumCircuit,
    a dictionary for the thetas used and a dictionary for the phi used in degrees)

    """
    def generateTests(self, testProperties: TestProperty):
        return [self.generateTest(testProperties) for _ in range(testProperties.noOfTests)]

