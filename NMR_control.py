#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 12:23:03 2020

@author: thomasmarsh
"""


from PyQt5 import QtWidgets, uic, QtCore
import sys
import pyvisa
import nidaqmx
import pprint

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Igor.ui', self)
        self.activate_buttons()
        self.show()
    
    def activate_buttons(self):
        self.run_nifid_button.clicked.connect(self.run_nifid)
        
    def run_nifid(self):
        freq = self.nifid_freq.value()
        width = self.nifid_pulselength.value()
        b_field = self.nifid_bfield.value()
        self.nifid_set_digital_io(1, 0)
    
        self.nifid_set_bfield(b_field)
        
    def nifid_set_digital_io(self, channel, value):
        print("Setting Digital IO")
        
    def nifid_set_bfield(self, b_field):
        print("Setting the B field")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()