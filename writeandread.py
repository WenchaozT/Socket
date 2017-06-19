#! /usr/bin/env python
#coding=utf-8

import serial
import signal
import time 
import string
import struct
from time import sleep 

flag_stop = False

def onsignal_int(a, b):
    print "sigint!"
    global flag_stop
    flag_stop = True

def cmd_write(sv):
    addr="8181"
    write="43"
    parameter="1a"
    value=hex(struct.unpack('>I',struct.pack('<I',10*sv))[0])
    str=value
    if sv>25:
        value=str[2:6]
    else:
        value=str[2:5]+"0"
    check=26*256+10*sv+67+1
    check=hex(struct.unpack('>I',struct.pack('<I',check))[0])
    str=check
    check=str[2:6]
    cmd_write=addr+write+parameter+value+check
    cmd_write=cmd_write.decode("hex")
    return cmd_write

signal.signal(signal.SIGINT, onsignal_int)
signal.signal(signal.SIGTERM, onsignal_int)

def readpv():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.15)   
    while True:
        cmd_read="8181520000005300"
        cmd_read=cmd_read.decode("hex") #发送十六进制字符串指令            
        s = ser.write(cmd_read)
        sleep(1) #向串口写指令，设置每一秒执行一次
        if flag_stop:               
            ser.write(stop)           
            print "reset cmd has been sent!"
            sleep(0.5)
            break
        time.localtime()
        time1 =time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()) #获取当前时间
    
        text = ser.read(10)    #读取仪器返回数据    
        cmd_back = text
        if len(cmd_back) < 2:   #判断返回是否为空     
            continue
        hex_list = [hex(ord(i)) for i in cmd_back] 
        str = hex_list
        pv1 = str[0]
        pv2 = str[1]
    
        temperature=256*(int(pv2,16))+int(pv1,16)
        temperature=temperature/10
    
        return temperature

def readsv():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.15) 
    while True:
        cmd_read="8181520000005300"
        cmd_read=cmd_read.decode("hex") #发送十六进制字符串指令            
        s = ser.write(cmd_read)
        if flag_stop:               
            ser.write(stop)           
            print "reset cmd has been sent!"
            sleep(0.5)
            break
       
        text = ser.read(10)    #读取仪器返回数据    
        cmd_back = text
        if len(cmd_back) < 2:   #判断返回是否为空     
            continue
        hex_list = [hex(ord(i)) for i in cmd_back] 
        str = hex_list
        sv1 = str[2]
        sv2 = str[3]
       
        givenvalue=256*(int(sv2,16))+int(sv1,16)
        givenvalue=givenvalue/10
          
        return givenvalue   
        

def writeT(sv):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.15)
    while True:
        write=cmd_write(sv)
        s = ser.write(write)
        if flag_stop:               
            ser.write(stop)           
            print "reset cmd has been sent!"
            sleep(0.5)
            break   
        text = ser.read(10)    #读取仪器返回数据    
        cmd_back = text
        if len(cmd_back) < 2:   #判断返回是否为空     
            continue
        hex_list = [hex(ord(i)) for i in cmd_back] 
        str = hex_list
        pv1 = str[0]
        pv2 = str[1]
        sv1 = str[2]
        sv2 = str[3]
        mv = str[4]
        alm = str[5]#提取所需要的值
        
        temperature=256*(int(pv2,16))+int(pv1,16)
        temperature=temperature/10
    
        givenvalue=256*(int(sv2,16))+int(sv1,16)
        givenvalue=givenvalue/10
        
        return givenvalue
       

if __name__=='__main__':
    writeT()
    readpv()
    readsv()