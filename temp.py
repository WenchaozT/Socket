#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import cgi

reshtml = '''Content-Type: text/html\n
<HTML><HEAD><TITLE>
Temp
</TITLE></HEAD>
<BODY><H3>��ѯ�û�Ϊ: <I>%s</I></H3>
��ѯʱ��� <B>%s</B> �� <B>%s</B>
<P>��ѯ���Ϊ: <P><H3><B>%s</B></H3><P>
</BODY></HTML>'''

errhtml = '''<H4><B>Content-Type: text/html\n
<HTML><HEAD><TITLE>
Temp
</TITLE></HEAD>
<BODY><H3>��ȡ����ʧ��:��������ȷ�����ݿ��û��������룡</H3>
</BODY></HTML>'''

form = cgi.FieldStorage()
who = form['userid'].value
startdate = form['startdate'].value
enddate = form['enddate'].value
dbuser = form['dbuser'].value
dbpassword = form['dbpassword'].value

def mysqlfetch(dbuser, dbpassword, startdate, enddate, who):
    """ ���ݿͻ��˸�������ݿ��û���Ϣ����ѯ��Ϣ��ȡ��Ӧ������."""

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
            return "û�з���������ֵ�������ѯ��Ϣ��"
        else:
            return results
        conn.close()
        
    except:
        return "��ȡ����ʧ��:�����û���Ϣ����ѯ��Ϣ��"

if dbuser=='' or dbpassword=='':
    print errhtml
else:
    myfetch = mysqlfetch(dbuser, dbpassword, startdate, enddate, who)
    print reshtml % (who, startdate, enddate, myfetch)