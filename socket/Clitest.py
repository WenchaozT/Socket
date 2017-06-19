#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from socket import *

HOST = '192.168.1.15'
PORT = 2016
BUFSIZ = 4096
ADDR = (HOST,PORT)

tempCli = socket(AF_INET, SOCK_STREAM)
tempCli.connect(ADDR)

while True:
    try:
        dbuser= raw_input(' input username\n> ')
        dbpassword = raw_input(' input password\n> ')
        dateinfo = raw_input('input startdate+enddate+username\neg:2016051612525020160528180000student\n> ')
        datalist = [dbuser, dbpassword, dateinfo]
        data = '|'.join(datalist)
        if not data:
            break
        tempCli.send(data)
        fetchdata = tempCli.recv(BUFSIZ)
        print fetchdata 
    except:   
        print u'提取数据失败'
    tempCli.close()

	
#2016051612000020160516125253student
