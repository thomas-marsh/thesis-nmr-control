
from PyQt5 import QtWidgets, uic, QtCore
import sys
import pyvisa
import nidaqmx
import pprint
import numpy as np
import matplotlib.pyplot as plt
import os
import time

wave = np.zeros(100)

other_wave = np.zeros(100)

for i in range(100):
    wave[i] = i*0.02
    if i % 2 == 0:
        other_wave[i] = True
    else:
        other_wave[i] = False

#Open a task for reading and writing using the NI board
with nidaqmx.Task() as task:
    #Write a waveform to the analog channel from device 1, port 0, line 4
    task.ao_channels.add_ao_voltage_chan("/Dev1/port0/line4")
    task.write(wave)
    
    #Write a waveform to a digital output channel (must be a boolean value)
    task.do_channels.add_do_chan("/Dev1/port0/line5")
    task.write(other_wave)
    
    #Write a constant value to a digital channel
    task.do_channels.add_do_chan("Dev1/do0")
    task.write(True)
    
    #Write a constant value to an analog channel
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    task.write(5)
    
    #Read from the given channel
    print(task.read())
    
    
#Using the GPIB for read/write
rm = pyvisa.ResourceManager()
print(rm.list_resources())

inst = rm.open_resource('GPIB0::10::INSTR')
#Ask for the GPIB information
print(inst.query("*IDN?"))
#Read the amplitude
inst.write('AMPL?')
print(inst.read())
#Read the frequency
inst.write('FREQ?')
print(inst.read())
#Set the amplitude 
inst.write("AMPL 1.00VP")


