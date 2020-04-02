# -*- coding: utf-8 -*-

import pyvisa
import nidaqmx
import pprint
import abc

pp = pprint.PrettyPrinter(indent=4)


#rm = pyvisa.ResourceManager()
#print(rm.list_resources())
#
#inst = rm.open_resource('GPIB0::10::INSTR')
#print(inst.query("*IDN?"))
#inst.write('AMPL?')
#print(inst.read())
#inst.write('FREQ?')
#print(inst.read())
#inst.write("AMPL 1.00VP")
#inst.write('AMPL?')
#print(inst.read())

#with nidaqmx.Task() as task:
#    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
#    
#    print('1 Channel 1 Sample Read Raw: ')
#    data = task.read()
#    pp.pprint(data)
    
    
class FID():
    pass
    
class GPIB_FID(FID):
    def __init__(self, gpib):
        self.gpib = gpib
        
    def run_FID(self, freq, pulse_length, ampl):
        self.gpib.set_freq(freq)
        self.gpib.set_ampl(ampl)
        #self.gpib.send_pulse(freq, ampl, pulse_length)
        #print(self.gpib.get_freq())
        #print(self.gpib.get_ampl())
        
        
class NI_FID(FID):
    def __init__(self, ni_board):
        self.ni_board = ni_board
        
class NI_Board():
    def __init__(self, name):
        self.name = name
        self.task = nidaqmx.Task()
        
    
        
        
class Generic_GPIB(abc.ABC):
    def get_ampl(self):
        return
    def set_ampl(self, value):
        pass
    def get_freq(self):
        return
    def set_freq(self, value):
        pass
    def set_func(self, form):
        pass
    
class DS345_GPIB(Generic_GPIB):
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(name + '::' + str(channel) + '::INSTR')

    def get_ampl(self):
        self.inst.write('AMPL?')
        return self.inst.read()
    def set_ampl(self, value):
        self.inst.write('AMPL ' + value + 'VP')
    def get_freq(self):
        self.inst.write('FREQ?')
        return self.inst.read()
    def set_freq(self, value):
        self.inst.write('FREQ ' + value)
    #square wave is 1
    def set_func(self, form):
        self.inst.write('FUNC ' + str(form))
        
my_fid = GPIB_FID(DS345_GPIB('GPIB0', 10))



my_fid.run_FID('100', 1, '1.00')

    
    
    
    
    
