from qiskit import *
from qiskit.quantum_info import Statevector

#From Marc
import parser

#From Luca
import socket
from SocketChannel2 import SocketChannel




class Channel:    
    def __init__(self,slave_offset=0, myport=000, remote_port=000):
        self._state_vector = None
        self._arr_qubits = None
        self._basis_gates = ['u1', 'u2', 'u3', 'cx','x','y','H','z']
        self._master = True
        self._offset = 0
        self._slave_offset = slave_offset

        self.realchannel = SocketChannel(myport, False)
        TCP_IP = '127.0.0.1'
        self.realchannel.connect(TCP_IP, remote_port)
        
        self._circuit = None
    
    def close(self):
        try:
            self.realchannel.kill()
        except:
            print("Exception: Thread still busy")

    def send(self,circuit,arr_qubits):
        self._state_vector = Statevector.from_instruction(circuit)  
        self._arr_qubits = arr_qubits
        self._circuit = circuit      
 
        #From Marc
        ser = parser.QSerializer()
        ser.add_element('state_vector', self._state_vector)#self)
        ser.add_element('is_master', self._master)#self)
        ser.add_element('slave_offset', self._slave_offset)#self)
        ser.add_element('is_master', self._master)#self)
        ser.add_element('circuit', self._circuit)#self)
        str_to_send = ser.encode()

        #print(str_to_send.type())

        #From Luca
        message = str_to_send

        channel = self.realchannel #SocketChannel()
        channel.send(message)
        channel.close()
        
        ## TODO: TCP THINGS
        return self
        
    def receive(self,circuit):#,recieve_channel):  ## TODO: remove recieve as an input
        #TODO: TCP things
        #recieve_channel = TCP_STUFF
        
        #From Luca
        print('Wait to receive')
        channel = self.realchannel #SocketChannel(port=5005, listen=True)
        data = channel.receive()
        # print("received stuff \o/")
        #print("received data:", data)
        channel.close()
        
        #From Marc
        ser2 = parser.QSerializer()
        ser2.decode(data)
        #recieve_channel = ser2.get_element('channel_class')
        
        self._slave_offset = ser2.get_element('slave_offset')
        if(ser2.get_element('is_master')):
            self._master = False
            self._offset = self._slave_offset
        
        recieved_state_vector = ser2.get_element('state_vector')
        new_circuit = QuantumCircuit(len(recieved_state_vector.dims()))
        new_circuit.initialize(recieved_state_vector.data, range(len(recieved_state_vector.dims())))
        new_circuit = transpile(new_circuit, basis_gates=self._basis_gates)
        new_circuit = new_circuit + circuit
        return ser2.get_element('circuit'), self._offset

        return new_circuit, self._offset   



