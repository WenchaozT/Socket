#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from socket import *
import time
import MySQLdb

def mysqlfetch(dbuser, dbpassword, dateinfo):
    """ 根据客户端给予的数据库用户信息及查询信息获取相应的数据."""
    startdate = dateinfo[0:14]
    enddate = dateinfo[14:28]
    username = dateinfo[28:]
    results = ''
    
    try:
        conn = MySQLdb.connect("localhost", dbuser, dbpassword, "TempMonitor")
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()
        #抓取所有符合条件的值
        cur.execute("select * from temptbl WHERE (temp_date >= %s\
                    and temp_date <= %s and username = '%s')"\
                    % (startdate, enddate, username))
        fetchresults = cur.fetchall()
        for row in fetchresults:
            tempid = row[0]
            tempdate = row[1]
            tempvalue = row[2]
            Username = row[3]
            settemp = row[4]
            results = results + '%s, %s, %s, %s, %s\n'\
            % (tempid, tempdate, tempvalue, Username, settemp)
        if not results:
            return "没有符合条件的值，请检查查询信息！"
        else:
            return results
        conn.close()
    except:
        return "提取数据失败:请检查用户信息及查询信息！"
    

HOST = ''
PORT = 2016
BUFSIZ = 4096
ADDR = (HOST,PORT)

tempSer = socket(AF_INET, SOCK_STREAM)
tempSer.bind(ADDR)
tempSer.listen(3)

while True:
      print '等待连接。。。'
      tempCli, addr = tempSer.accept()
      print ' ...连接：', addr, time.strftime('%m/%d %H:%M:%S')
      
      while True:
            data = tempCli.recv(BUFSIZ)
            if not data:
                break
            datalist = data.split('|')
            dbuser = datalist[0]
            dbpassword = datalist[1]
            dateinfo = datalist[2]
            print dbuser,dateinfo,time.strftime('%m/%d %H:%M:%S'),"\n"
            tempCli.send(mysqlfetch(dbuser, dbpassword, dateinfo))

tempSer.close()
