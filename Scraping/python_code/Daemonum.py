# Rachael Carpenter
# 1/9/2022
#
# Quantum Daemonum 
# A simple game where you play as as a wicked spirit in a battle with
# Van Helsing who happens to have a quantum computer. Van Helsing will
# attempt to guess your true name in an attempt to gain power over and
# and defeat you. You can attempt to thwart him with spiritual attacks.
#


import random
import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit.providers.aer import QasmSimulator
import operator
import math
import numpy as np


                                                                                
# This function is called when its time to use the quantum simulator
def runGame(program):
    shots = 100
    # execute program on quantum simulator
    job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'), shots=shots)
    result = job.result().get_counts()
    return result



# utility function called by quantumGuess
def quantumProcessing(quessProcess, qreg, hiddenName):
    # Convert hiddenName in binary from list to array
    secretName = list(hiddenName)

    # reverse order of bits
    secretName.reverse()
    indexList = []

    # find indices of all zeroes
    for i in range(len(secretName)):
        if (secretName[i] == '0'):
            indexList.append(i)

    # Invert the 0s
    for i in range(len(indexList)):
        # find bits with a value of 0
        anIndex = indexList[i]
        
        # Invert qubit
        quessProcess.x(qreg[anIndex])
        

    
# This function handles the quantum and classical registers and manipulates them
# to perform Grover's search algorithm.
def quantumGuess(hiddenName):
    # 4-bit Grover's search to identify target index of 4 bits from list of all combinations of 4 bits
    # create 2 qubits for input
    qreg = QuantumRegister(4)
    # these 2 registers take output
    creg = ClassicalRegister(4)
    guessProcess = QuantumCircuit(qreg, creg)

    # place qubits into superposition, representing all possible outcomes(starting position)
    guessProcess.h(qreg)
   
    # Run quantumProcessing on key, inverting bits with value of zero
    quantumProcessing(guessProcess, qreg, hiddenName) 
    
    #Grover's Algorithm
    guessProcess.cp(np.pi / 4, qreg[0], qreg[3])
    guessProcess.cx(qreg[0], qreg[1])
    guessProcess.cp(-np.pi / 4, qreg[1], qreg[3])
    guessProcess.cx(qreg[0], qreg[1])
    guessProcess.cp(np.pi / 4, qreg[1], qreg[3])
    guessProcess.cx(qreg[1], qreg[2])
    guessProcess.cp(-np.pi / 4, qreg[2], qreg[3])
    guessProcess.cx(qreg[0], qreg[2])
    guessProcess.cp(np.pi / 4, qreg[2], qreg[3])
    guessProcess.cx(qreg[1], qreg[2])
    guessProcess.cp(-np.pi / 4, qreg[2], qreg[3])
    guessProcess.cx(qreg[0], qreg[2])
    guessProcess.cp(np.pi / 4, qreg[2], qreg[3])
   
    #Reverse the earlier inversions by guessProcessing
    quantumProcessing(guessProcess, qreg, hiddenName)

    #Amplification
    guessProcess.h(qreg)
    guessProcess.x(qreg)

    #apply grover's algorithm again for amplification
    guessProcess.cp(np.pi / 4, qreg[0], qreg[3])
    guessProcess.cx(qreg[0], qreg[1])
    guessProcess.cp(-np.pi / 4, qreg[1], qreg[3])
    guessProcess.cx(qreg[0], qreg[1])
    guessProcess.cp(np.pi / 4, qreg[1], qreg[3])
    guessProcess.cx(qreg[1], qreg[2])
    guessProcess.cp(-np.pi / 4, qreg[2], qreg[3])
    guessProcess.cx(qreg[0], qreg[2])
    guessProcess.cp(np.pi / 4, qreg[2], qreg[3])
    guessProcess.cx(qreg[1], qreg[2])
    guessProcess.cp(-np.pi / 4, qreg[2], qreg[3])
    guessProcess.cx(qreg[0], qreg[2])
    guessProcess.cp(np.pi / 4, qreg[2], qreg[3])

    # Reverse amplification
    guessProcess.x(qreg)
    guessProcess.h(qreg)

    # Measure results
    guessProcess.barrier(qreg)
    guessProcess.measure(qreg, creg)

    # 'results' can be printed to check for error
    results = runGame(guessProcess)
    foundName = max(results.items(), key=operator.itemgetter(1))[0]

    # convert binary result to character array
    resultArray = list(foundName)

    # convert character array in integers
    resultArrayInt = [int(i) for i in resultArray]
    stringy = ''.join([str(item) for item in resultArrayInt])
    
    #convert result to index in name array
    myIndex = int(stringy, 2)
    return myIndex
    

# list of names is accessed by index in list
def getDemonName(index):
    demonNames = {
        1:'Dusios',
        2:'Belial',
        3:'Belphegor', 
        4:'Andromalius',
        5:'Astaroth',
        6:'Beleth',
        7:'Drekevac',
        8:'Demiurge',
        9:'Forneus',
        10:'Gomory',
        11:'Haures',
        12:'Pithius',
        13:'Mammon',
        14:'Marchosias',
        15:'Moloch',
        16:'Naphula'
    }
    return demonNames.get(index)


# This function returns text based on game status variables.
def battleStatus(evil, good):
    if good > 50 and good < 100 and evil <= 50:
        return 'Dr. Van Helsing is fiddling will a strange quantum device. Your powers are weak.'
    elif evil <= 50 and good == 100:
        return 'A blast of light fills the cavern.' 
    elif good > 75:
        return 'The quantum device is flickering with light and emits steam.'
    elif evil <= 50 and good <= 50:
       return 'Dr. Van Helsing is experiencing technical issues.'
    elif evil == 100:
        return 'Your are powers have returned.'
    elif evil >= 50 and good >= 50:
        return 'Your powers are growing stronger. The machine sparkling with electricity.'


# This function returns text that is printed describing effects after player input.
def statusChange(actionCode):
    if actionCode == 5:
        return ' '
    elif actionCode == 4:
        return 'The cavern glows with a red light.'
    elif actionCode == 3:
        return 'A thick fog fills the cavern.'
    elif actionCode == 1:
        return 'Nothing happens.'


# Processes main player input each turn.
def action(read):
    read = str(read)
    read = read.lower()
    switcher = {
        'p': 5, #possess, requires high evil
        'd': 4, #duplici, increase evil, 
        'v': 3, #vaporum, decrease good, VH requires high good for quantum guess
                    #VH will increase good each turn until he can attack
        'n': 1, #nothing
        'q': 0  #quit
    }    
    return switcher.get(read[0], -1)


# Processes player input at end of game.
def response(read):
    read = str(read)
    read = read.lower()
    switcher = {
        'y': 1,
        'n': 0,
        'q': 0
    }
    return switcher.get(read, -1)


# The main function; contains main game loop.
def main():
    #print welcome message
    print("")
    print("   __                 ___                __        ___        __")
    print("  /  \ |  |  /\  |\ |  |  |  |  |\/|    |  \  /\  |__   |\/| /  \ |\ | |  |  |\/|")
    print("  \__X \__/ /~~\ | \|  |  \__/  |  |    |__/ /~~\ |___  |  | \__/ | \| \__/  |  |")
    print("           ~ A DARK GAME PLAYED AGAINST A SIMULATED QUANTUM COMPUTER ~\n\n")
    print(" The year is 1887. You are a wicked spirit, evil personified, who is being hunted")
    print(" by Van Helsing, the infamous slayer of unholy beasts. He will try to destroy you by")
    print(" guessing your true name. You must stop him at any cost. A battle of magic and wits")
    print(" begins! Van Helsing has you cornered in the caverns below Corvin Castle in Romania.")
    print(" He performs the rites of excorcism while you have three spells.\n\n")
    print(" Use keyboard commands to attempt to thwart Van Helsing, who makes guesses using")
    print(" Grover's search algorithm, which runs on a quantum simulator.\n")

    # controls main game loop which accomodates multiple interior loops for each round of play
    quitGame = False    
    
    #Begin main loop of program
    while not quitGame:
        # pick the true name for this game from name array
        playerName = random.randint(0, 15)
        trueName = getDemonName(playerName + 1)
        print(" Your true name is ... " + str(trueName) + "\n")
    
        # convert player name index int to binary
        secretBinary = format(playerName, "04b")

        gameOver = False     # controls whether main loop game runs
        evil = 0             # evil level 100 allows posession to occur
        good = 50            # good level 100 needed for quantum divination
        loopControl = 1      # counts number of rounds of battle in each game

        # controls for good and evil status/level changes
        evilIncrease = -1    
        goodDecrease = -1
        VHCasting = 5

        # begin main loop for this round of play
        while not gameOver and not quitGame:
            # controls whether Van Helsing uses quantum guessing this round
            VHActive = True 
            print(" +:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+\n") 
            
            # manage status changes for this turn
            if VHCasting > 0:
                good = good + random.randint(10,45)
                if good > 100:
                    good = 100
            if evilIncrease > -1:
                evil = evil + random.randint(1,50)
                evilIncrease = evilIncrease - 1
                if evil > 100:
                    evil = 100
            if goodDecrease > -1:
                good = good - random.randint(1,40)
                goodDecrease = goodDecrease - 1
                if good < 0:
                    good = 0

            # print stats for this round        
            roundStr = str(loopControl)          
            evilStr = str(evil)
            print(" Round: ", roundStr.rjust(5))
            print(" Evil : ", evilStr.rjust(5))
            goodStr = str(good)
            print(" Good : ", goodStr.rjust(5))
            print("\n " + battleStatus(evil, good))

            # this variable takes resulting index indicating the resulting name of quantum guess
            VHResult = -1

            #process on quantum simulator, VH will guess now
            if VHActive and good == 100:
                #let the computer guess
                VHResult = quantumGuess(secretBinary)
            #check player progress
            if  (VHResult != -1 and str(getDemonName(VHResult+1)) == str(trueName)):
                gameOver = True
                print(" The strange device spits out a slip of paper.")
                print(" Van Helsing reads the paper aloud in a booming voice: \"" + getDemonName(VHResult+1) + "!\"")
                print(" All your power is obliterated. GAME OVER.")
            if VHResult != -1 and str(getDemonName(VHResult+1)) != str(trueName):
                print(VHResult+1)
                print(" The strange device spits out a slip of paper.")
                print(" Van Helsing reads the paper aloud in a booming voice: \"" + getDemonName(VHResult+1) + "!\"")
                print(" Quantum algorithms fail sometimes...")
            
            # get player input for this turn
            if gameOver == False:
                read = '' # text of input will be stored here
                while not read.lower() in ['p','d','v','f','n','q','possess','duplici','vaporum','nothing','quit']:
                    read = input("\n [Possess(p), Duplici(d), Vaporum(v), nothing(n), quit(q)]: ").lower()
                #process input
                actionCode = -1
                actionCode = action(read)
                if actionCode == 5: #possession
                    if evil == 100:
                        gameOver = True
                        print("\n Van Helsing's soul withers as you take over his physical form.")
                        print(" You destroy the machine and escape the cavern. THE END.")
                    else:
                        print("\n You are too weak to possess Van Helsing.")
                elif actionCode == 4: # Duplici, evil increases for some random amount of turns
                    evilIncrease = random.randint(1, 5)
                elif actionCode == 3: # Vaporum, good decreases for some random amount of turns
                    VHActive = False
                    goodDecrease = random.randint(1, 5)
                elif actionCode == 0: # quit
                    quitGame = True
                    break
                # report evil/good status changes from the last turn
                print("\n " + statusChange(actionCode))
                loopControl = loopControl + 1


            # end game menu, take user input
            if gameOver == True:
                read = ''
                while not read.lower() in ['y','n','q','yes','no','quit']:
                    #Read input from user
                    read = input("\n +:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+\n" +
                             " Do you want to play again?"+
                              "\n [yes(y), no(n), quit(q)]: ").lower()
                    #process input        
                    actionCode = -1
                    actionCode = response(read)
                    if actionCode == 0:
                        quitGame = True
                        break
                    elif actionCode == 1:
                        loopControl = 1
                        gameOver == False
                    else:
                        print(" What?")
        

# run main function
if __name__ == "__main__":
    main()
    
    
