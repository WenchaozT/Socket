#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import cgi

reshtml = '''Content-Type: text/html\n
<HTML><HEAD><TITLE>
Temp
</TITLE></HEAD>
<BODY><H3>查询用户为: <I>%s</I></H3>
查询时间从 <B>%s</B> 至 <B>%s</B>
<P>查询结果为: <P><H3><B>%s</B></H3><P>
</BODY></HTML>'''

errhtml = '''<H4><B>Content-Type: text/html\n
<HTML><HEAD><TITLE>
Temp
</TITLE></HEAD>
<BODY><H3>提取数据失败:请输入正确的数据库用户名和密码！</H3>
</BODY></HTML>'''

form = cgi.FieldStorage()
who = form['userid'].value
startdate = form['startdate'].value
enddate = form['enddate'].value
dbuser = form['dbuser'].value
dbpassword = form['dbpassword'].value

def mysqlfetch(dbuser, dbpassword, startdate, enddate, who):
    """ 根据客户端给予的数据库用户信息及查询信息获取相应的数据."""

    try:
        conn = MySQLdb.connect("localhost",dbuser, dbpassword, "test")
        cur = conn.cursor()
        cur.execute("select * from testmodel_test WHERE (tempdate >= %s\
            and tempdate <= %s and userid = '%s')"% (startdate, enddate, who))
        fetchresults = cur.fetchall()
        results = ''
        for row in fetchresults:
            tempid = row[0]
            userid = row[1]
            tempvalue = row[2]
            tempdate = row[3]
            settemp = row[4]
            results = results + '%s, %s, %s, %s, %s <P>' % (tempid, userid, tempvalue, tempdate, settemp)
        if not results:
            return "没有符合条件的值，请检查查询信息！"
        else:
            return results
        conn.close()
        
    except:
        return "提取数据失败:请检查用户信息及查询信息！"

if dbuser=='' or dbpassword=='':
    print errhtml
else:
    myfetch = mysqlfetch(dbuser, dbpassword, startdate, enddate, who)
    print reshtml % (who, startdate, enddate, myfetch)