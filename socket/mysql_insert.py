#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import MySQLdb
import serial
import signal 
import string
from time import sleep 
import math

username = 'student'
flag_stop = False


# 打开数据库连接
conn = MySQLdb.connect("192.168.1.15","tang","tang","TempMonitor")

def mysqlinsert(username,tempvalue,settemp):
    #username = 'student'
    #tempvalue = 299
    tempdate =time.strftime("%Y%m%d%H%M%S")

    # 使用cursor()方法获取操作游标
    cur = conn.cursor()
    if username =='student':
        try:
            cur.execute("INSERT INTO temptbl(temp_date, temp_value, settemp)\
                      VALUES(%s, %s, %s)"  % (tempdate, tempvalue, settemp))
            conn.commit()
        except:
            conn.rollback()
    else:
        try:
            cur.execute("INSERT INTO temptbl(temp_date, temp_value, username, settemp)\
                VALUES(%s, %s, '%s', %s)" % (tempdate, tempvalue, username, settemp))
            conn.commit()
        except:
            conn.rollback()
    
    
def onsignal_int(a, b):
    print "sigint!"
    global flag_stop
    flag_stop = True

signal.signal(signal.SIGINT, onsignal_int)
signal.signal(signal.SIGTERM, onsignal_int)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.15)
print "serial.isOpen() =", ser.isOpen()

cmd_send = "8181520000005300"
cmd_send = cmd_send.decode("hex") #发送十六进制字符串指令

cmd_back = ""
cmd_count = 0x00

while True:
    s = ser.write(cmd_send)
    sleep(1) #向串口写指令，设置每一秒执行一次
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
    
    temp = 100*int(pv2,16) + int(pv1,16)
    tempvalue = (temp/10)
    given = 100*int(sv2,16) + int(sv1,16)
    settemp = (given/10)
    mysqlinsert(username,tempvalue,settemp)
    cmd_count += 1
ser.close()

# 关闭数据库连接
conn.close()
