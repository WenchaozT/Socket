#! /usr/bin/env python
#coding=utf-8
import writeandread
import serial
import signal
from time import sleep 

flag_stop = False

def onsignal_int(a, b):
    print "sigint!"
    global flag_stop
    flag_stop = True

signal.signal(signal.SIGINT, onsignal_int)
signal.signal(signal.SIGTERM, onsignal_int)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.15)

while True:
    a=writeandread.readpv()
    b=writeandread.readsv()
    sleep(1)
    print"pv=",a
    print"sv=",b


