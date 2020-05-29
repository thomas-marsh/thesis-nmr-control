#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, uic, QtCore
import sys
import pyvisa
import nidaqmx
import pprint
import numpy as np
import matplotlib.pyplot as plt
import os


"""

NMR Control Software
May, 2020
Thomas Marsh, Gordon Jones, Brian Collett
Hamilton College

Read the included documentation for the current state and other useful details

For read/write examples, see io_examples.py
    



"""

#Set to false if you are not testing with actual equipment attached
devices_connected = False


#Main class that sets up the user interface
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('nmr_control.ui', self)
        self.activate_buttons()
        self.show()
    
    #This method is where all button linkups are made for the UI
    def activate_buttons(self):
        self.run_nifid_button.clicked.connect(self.run_nifid)
        
    #Method for running an NIFID
    # closely mimics the structure of the Igor code
    def run_nifid(self):
        freq = self.nifid_freq.value()
        width = self.nifid_pulselength.value()
        b_field = self.nifid_bfield.value()
        rf_amp = self.nifid_rfamp.value()
        t_mute = self.nifid_mutetime.value()
        t_read = self.nifid_readout.value()
        
        self.nifid_set_digital_io(0, True)
    
        self.nifid_set_bfield(b_field)
        
        self.nifid_dsp_pulse(freq, width, rf_amp, t_mute, t_read)
        
        self.nifid_set_digital_io(0, False)
        
    
    #Sets the digital output channel to a given value (boolean)
    def nifid_set_digital_io(self, channel, value):
        print("Setting Digital IO")
        if devices_connected:
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan("Dev1/do" + str(channel))
                task.write(value)
        
        
    def nifid_set_bfield(self, b_field):
        print("Setting the B field")
        port_num = 1
        if devices_connected:
            with nidaqmx.Task() as task:
                task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
                task.write(b_field)
            
    def nifid_dsp_pulse(self, freq, width, rf_amp, t_mute, t_read):
        print("Sending DSP Pulse")
        ao_time_step = 2.7e-6
        ai_time_step = 2.7e-6
        low_pass = self.nifid_lowpass.value()
        signal_size = self.nifid_signalrange.value()
        mute_bar_chan = 7
        mute_chan = 4
        pulse1_chan = 6
        pulse2_chan = 5
        mute_time = t_mute + width
        lockin_mode = self.lockin_mode.currentIndex() + 1
        rf_mode = self.rf_mode.currentIndex() + 1

        if mute_time < 0:
            mute_time = 0
            
        if lockin_mode == 2:
            self.fit_type.setCurrentText('SineX')
            
        if rf_mode == 2:
            print("aCORN")
            #Do FID with GPIB
            self.gpib_init()
            
            
        #num_pts = round(width / ao_time_step)
            
        out_pts = np.arange(0, width, ao_time_step)
        out_wave = rf_amp * np.sin(2 * np.pi * freq * out_pts)
        wave_len = len(out_wave)
        out_wave[wave_len-5] = out_wave[wave_len-6]*np.exp(-0.5)
        out_wave[wave_len-4] = out_wave[wave_len-6]*np.exp(-1)
        out_wave[wave_len-3] = out_wave[wave_len-6]*np.exp(-1.5)
        out_wave[wave_len-2] = out_wave[wave_len-6]*np.exp(-2)
        out_wave[wave_len-1] = 0
        
        daq_x_up = np.arange(0, t_read, ai_time_step)
        daq_y_up = np.arange(0, t_read, ai_time_step)
        
        clock_step = ai_time_step
        #clock_step = 1e-5
        
        wave_size = round(max(mute_time, width)/clock_step) + 100
        pulse1_wave = np.zeros(wave_size)
        pulse2_wave = np.zeros(wave_size)
        mute_wave = np.zeros(wave_size)
        mute_bar_wave = np.ones(wave_size)
        
        for i in range(int(width / clock_step)):
            pulse1_wave[i] = True
            pulse2_wave[i] = True
        
        for i in range(int(mute_time / clock_step)):
            mute_bar_wave[i] = False
            mute_wave[i] = False
            
        if devices_connected:
            print("Send waves to device")
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan('/Dev1/port0/line' + str(pulse1_chan))
                task.write(pulse1_wave)
                
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan('/Dev1/port0/line' + str(pulse2_chan))
                task.write(pulse2_wave)
                
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan('/Dev1/port0/line' + str(mute_chan))
                task.write(mute_wave)
                
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan('/Dev1/port0/line' + str(mute_bar_chan))
                task.write(mute_bar_wave)
                
        if rf_mode == 1:
            print('Use DAQ for RF')
            
    def gpib_init(self):
        print('initializing gpib')
    
        
            

app = QtWidgets.QApplication(sys.argv)
window = Ui()

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

#Code that should help with scaling the 
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# hint = app.sizeHint()
# if hint.isValid():
#     app.setMinimumSize(hint)
    
app.exec_()