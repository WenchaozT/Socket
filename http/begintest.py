#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import cgi
import time
from writeandread import *
from read_pv_sv import *
import signal
from time import sleep 

flag_stop = False


form = cgi.FieldStorage()
username = form['userid'].value
sampl = form['sampl'].value
settemp = form['enddate'].value
dbuser = form['dbuser'].value
dbpassword = form['dbpassword'].value

reshtml = ''' <H4><B>Content-Type: text/html\n
<HTML><HEAD><TITLE>
Temp
</TITLE></HEAD>
<BODY><H3>写入成功！</H3>
</BODY></HTML>'''
errhtml = '''<H4><B>Content-Type: text/html\n
<HTML><HEAD><TITLE>
Temp
</TITLE></HEAD>
<BODY><H3>写入失败！</H3></BODY></HTML>
'''

def mysqlinsert(username, settemp, tempvalue):

    tempdate =time.strftime("%Y%m%d%H%M%S")

    # 使用cursor()方法获取操作游标
    cur = conn.cursor()
    if username =='student':
        try:
            cur.execute("INSERT INTO testmodel_test(temp_date, temp_value, settemp)\
                      VALUES(%s, %s, %s)"  % (tempdate, tempvalue, settemp))
            conn.commit()
        except:
            conn.rollback()
    else:
        try:
            cur.execute("INSERT INTO testmodel_test(temp_date, temp_value, username, settemp)\
                VALUES(%s, %s, '%s', %s)" % (tempdate, tempvalue, username, settemp))
            conn.commit()
        except:
            conn.rollback()

#将设定值传给仪器
def givetemp():
    return int(settemp)


flag_stop = False

def onsignal_int(a, b):
    print "sigint!"
    global flag_stop
    flag_stop = True
    
signal.signal(signal.SIGINT, onsignal_int)
signal.signal(signal.SIGTERM, onsignal_int)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 0.15)

while True:
    tempvalue = writeandread.readpv()
    sleep(1)
    try:
        conn = MySQLdb.connect("192.168.1.23", dbuser, dbpassword, "test")
        myinsert = mysqlinsert(username, settemp, tempvalue)
        sleep(1)
        print reshtml
    except:
        print errhtml


