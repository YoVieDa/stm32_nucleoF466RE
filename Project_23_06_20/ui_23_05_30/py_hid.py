# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys, os, serial, serial.tools.list_ports, warnings
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
from PyQt5.QtWidgets import *
import py_button_react as br


USB_VENDOR  = 0x0483
USB_PRODUCT = 0x5750

result = []
portindex = 0

usb_code = [
    [0, 0, 0],       # {WBA}                         Send [0, 0, 0] to MCU by USB       0
    [0, 0, 1],       # {WB1}                         Send [0, 0, 1] to MCU by USB       1
    [0, 0, 2],       # {WB2}                         Send [0, 0, 2] to MCU by USB       2
    [0, 0, 3],       # {WB3}                         Send [0, 0, 3] to MCU by USB       3
    [0, 1, 0],       # {RBA}                         Send [0, 1, 0] to MCU by USB       4
    [0, 1, 1],       # {RB1}                         Send [0, 1, 1] to MCU by USB       5
    [0, 1, 2],       # {RB2}                         Send [0, 1, 2] to MCU by USB       6
    [0, 1, 3],       # {RB3}                         Send [0, 1, 3] to MCU by USB       7

    [0, 2, 0],       # Start Infinite Loop Plot      Send [1, 0, 1] to MCU by USB       8
    [0, 2, 1],       # Start Infinite Loop Plot      Send [1, 0, 1] to MCU by USB       9
    [0, 2, 2],       # Stop Infinite Loop Plot       Send [1, 0, 2] to MCU by USB       10

    [0, 3, 1],       # Generate 1 Random Table1      Send [2, 0, 1] to MCU by USB       11
    [0, 3, 2],       # Generate 1 Random Table2      Send [2, 0, 2] to MCU by USB       12
    [0, 3, 3],       # Generate 1 Random Table3      Send [2, 0, 2] to MCU by USB       13
    [0, 3, 4],       # Generate 1 Random Table4      Send [2, 0, 2] to MCU by USB       14
    [0, 3, 5],       # Generate 1 Random Table5      Send [2, 0, 2] to MCU by USB       15
    [0, 3, 6],       # Generate 1 Random Table6      Send [2, 0, 2] to MCU by USB       16
    [0, 3, 7],       # Generate 1 Random Table7      Send [2, 0, 2] to MCU by USB       17
    [0, 3, 8],       # Generate 1 Random Table8      Send [2, 0, 2] to MCU by USB       18
    [0, 3, 9],       # Generate 1 Random Table9      Send [2, 0, 2] to MCU by USB       19
    [0, 3, 10],      # Generate 1 Random Table10     Send [2, 0, 2] to MCU by USB       20

    [0, 4, 0],       # Loop the USB                  Send [3, 0, 0] to MCU by USB       21
    [0, 4, 1],       # Generate random once          Send [3, 0, 0] to MCU by USB       22
    [0, 4, 2],       # Generate random many times    Send [3, 0, 0] to MCU by USB       23
    [0, 4, 3],       # Stop random many times        Send [3, 0, 0] to MCU by USB       24
]

###########################################################################################################
# QT Main
###########################################################################################################
def prep_usb(ui, mytext_ascii):
    ui.usb_task = 0
    mytext_byte = []

    mytext_byte.append(0)       # this index must append because the first index will not read in microprocessor
    mytext_ascii = mytext_ascii[5:len(mytext_ascii)]
    separatePosition = mytext_ascii.find(";")

    count_data = 0
    while separatePosition > -1:        # start loop as much as value has been sent
        separatePosition = mytext_ascii.find(";")
        data = br.integer_to_byte(int(mytext_ascii[0:separatePosition]))        # get token of value and convert to byte data
        for j in range(2):
            mytext_byte.append(data[j])
        mytext_ascii = mytext_ascii[separatePosition + 1:len(mytext_ascii)]     # update mytext_ascii
        count_data += 1

    # after out of loop, one data which have no separate ; will handle in under this.
    separatePosition = mytext_ascii.find("}")
    if separatePosition != -1:
        data = br.integer_to_byte(int(mytext_ascii[0:separatePosition]))        # get token of value and convert to byte data
        for j in range(2):
            mytext_byte.append(data[j])
        count_data += 1

    return mytext_byte

def prep_usb_random64 ():
    arr = [0]
    for i in range (64):
        arr.append(i)

    return arr

def send_to_mcu_by_usb(ui, signal):
    ui.device.write(usb_code[signal])

    # wait
    time.sleep(0.01)

def read_from_mcu_by_usb(ui):
    # receive 64 data from MCU
    data = ui.device.read(65)

    return data

def read_from_mcu_by_usb_config(ui):
    # receive 64 data from MCU
    data = ui.device.read(65)

    if data:  # If data detected, do this...
        #print(data)

        start = 1  # start index to convert data from MCU to integer

        for i in range(10):  # convert data to integer and put to form
            res1 = int.from_bytes(data[start:start + 2], "little")
            res2 = int.from_bytes(data[(start + 20):(start + 22)], "little")
            res3 = int.from_bytes(data[(start + 40):(start + 42)], "little")

            if res1 > 32767:
                res1 = res1 - 65536
            if res2 > 32767:
                res2 = res2 - 65536
            if res3 > 32767:
                res3 = res3 - 65536

            ui.input1[i].setText(str(res1))
            ui.input2[i].setText(str(res2))
            ui.input3[i].setText(str(res3))

            start += 2

    else:       # Data not detected
        print("read fail")

    time.sleep(0.05)    # Wait

def usb_change_signal(ui, signal):
    ui.usb_task = signal