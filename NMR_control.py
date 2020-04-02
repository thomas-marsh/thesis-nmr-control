#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 12:23:03 2020

@author: thomasmarsh
"""


from PyQt5 import QtWidgets, uic
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Igor.ui', self)
        self.activate_buttons()
        self.show()
    
    def activate_buttons(self):
        self.run_nifid_button.clicked.connect(self.run_nifid)
        
    def run_nifid(self):
        print("test")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()