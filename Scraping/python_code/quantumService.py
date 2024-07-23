import time
from qiskit_ibm_runtime import QiskitRuntimeService
import qiskit
import qiskit_ibm_runtime
import qiskit_aer
import numpy as np
import random as rand
import os


# Projecting Quantum class

class Quantum:
    def __init__(self, gStack, qbCount):
        self.id = 0
        self.qiskitVersion = qiskit.__version__
        self.imagesPath = "./Images" # Folder to Images
        self.loggerPath = "./Logger" # Folder to Loggs

        self.gatesStack = gStack # Stack of the gates
        self.qubitsCount = qbCount # count of the qubits

        # Registers
        self.regQ = qiskit.QuantumRegister(self.qubitsCount, "QRegister") # Quantum
        self.regC = qiskit.ClassicalRegister(self.qubitsCount, "CRegister") # Classic

        self.circuit = qiskit.QuantumCircuit(self.regQ, self.regC) # Circuit

        self.gates = ["h", "x", "z", "ry", "cx", "cu3", "ccx"]

    # Ibm connection
    def connIBMService(self):
        QiskitRuntimeService.save_account(
            channel="channel",
            name="name",
            token="token",
            set_as_default=True
        )
        return QiskitRuntimeService()
    def connectBack(self, serviceIBM):
        print(serviceIBM)
        return serviceIBM.backend("quantum device")

    # Logic
    def findId(self):
        self.id += 1
        return time.ctime().replace(" ", "_").replace(":", "-") + "_" + str(self.id)
    def saveImage(self, name):
        self.circuit.draw(output='mpl', filename=self.imagesPath + "/" + name)

    def loggCircuit(self, name):
        file_path = os.path.join(self.loggerPath, f"{name}.txt")
        fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o666)
        try:
            with os.fdopen(fd, 'w') as openedFile:
                for el in self.gatesStack:
                    newRow = ""
                    for row in el:
                        newRow += str(row) + ", "
                    openedFile.write(newRow + '\n')  # Add a newline after each row for better readability
        except Exception as e:
            raise e

    def isInCircuit(self, qubitIdList):
        for qubitId in qubitIdList:
            if not (qubitId > 0 and qubitId < self.qubitsCount):
                return False
        return True

    # Using of the gates
    def useGate(self, gateElement):
        gate = gateElement[0]

        if (gate == "h"):
            if len(gateElement) != 2:
                print("Gate h has 1 param.")
                return

            self.isInCircuit(gateElement[1:])
            self.circuit.h(self.regQ[gateElement[1]]) # ("h", 1,)
        elif (gate == "x"):
            if len(gateElement) != 2:
                print("Gate x has 1 param.")
                return

            self.isInCircuit(gateElement[1:])
            self.circuit.h(self.regQ[gateElement[1]]) # ("x", 1,)
        elif (gate == "z"):
            if len(gateElement) != 2:
                print("Gate z has 1 param.")
                return

            self.isInCircuit(gateElement[1:])
            self.circuit.h(self.regQ[gateElement[1]]) # ("z", 1,)
        elif (gate == "ry"):
            if len(gateElement) != 3:
                print("Gate ry has 2 params.")
                return

            self.isInCircuit(gateElement[1:2])
            self.circuit.ry(2*gateElement[2], self.regQ[gateElement[1]]) # ("ry", 1, 45)
        elif (gate == "cx"):
            if len(gateElement) != 3:
                print("Gate cx has 2 params.")
                return

            self.isInCircuit(gateElement[1:3])
            self.circuit.cx(self.regQ[gateElement[1]], self.regQ[gateElement[2]]) # ("cx", 1, 2)
        elif (gate == "cu3"):
            if len(gateElement) != 4:
                print("Gate cu3 has 3 params.")
                return

            self.isInCircuit(gateElement[1:3])
            self.circuit.cu3(self.regQ[gateElement[3]], 0, 0, self.regQ[gateElement[1]], self.regQ[gateElement[2]]) # ("cu3", 1, 2, 45)
        elif (gate == "ccx"):
            if len(gateElement) != 4:
                print("Gate ccx has 3 params.")
                return

            self.isInCircuit(gateElement[1:4])
            self.circuit.ccx(self.regQ[gateElement[1]], self.regQ[gateElement[2]], self.regQ[gateElement[3]]) # ("ccx", 1, 2, 3)
        else:
            print("Doesn't found gate: " + gate)
            return None
        return gate

    def run(self):
        self.regQ = qiskit.QuantumRegister(self.qubitsCount, "QRegister")  # Quantum
        self.regC = qiskit.ClassicalRegister(self.qubitsCount, "CRegister")  # Classic
        self.circuit = qiskit.QuantumCircuit(self.regQ, self.regC)

        for el in self.gatesStack:
            result = self.useGate(el)
            if result == None:
                return
            else:
                # print("Operator - " + result + " - used.")
                pass
        self.build()

    def build(self):
        self.circuit.measure(self.regQ, self.regC)
        print("Circuit was measured.")

        idOfJob = self.findId()
        print("Created job: " + idOfJob)

        self.saveImage(idOfJob)
        self.loggCircuit(idOfJob)

        job = qiskit_aer.AerSimulator(method='automatic').run(self.circuit, shots=1024)
        # get the result
        counts = job.result().get_counts(self.circuit)
        print(counts)

    def setupNewStack(self, newGatesStack):
        self.gatesStack = newGatesStack

stackOfGates = [["h", 1],["h", 2],["h", 3],["ccx", 4, 1, 2]]
quantum = Quantum(stackOfGates, 5)
quantum.run()

quantum.setupNewStack([["h", 1],["h", 2],["h", 2],["ccx", 0, 1, 4]])
quantum.run()
quantum.run()
