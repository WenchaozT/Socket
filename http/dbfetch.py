#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def dbfetch(dbuser, dbpassword, dateinfo):
    """ ���ݿͻ��˸��������ݿ��û���Ϣ����ѯ��Ϣ��ȡ��Ӧ������."""
    startdate = dateinfo[0:14]
    enddate = dateinfo[14:28]
    username = dateinfo[28:]
    results = ''
    
    try:
        conn = MySQLdb.connect("localhost", dbuser, dbpassword, "TempMonitor")
        # ʹ��cursor()������ȡ�����α�
        cur = conn.cursor()
        #ץȡ���з���������ֵ
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
            return "û�з���������ֵ����������ѯ��Ϣ��"
        else:
            return results
        conn.close()
    except:
        return "��ȡ����ʧ��:�������û���Ϣ����ѯ��Ϣ��"
        
#userid=user_id and tempdate>=start_date and tempdate<=end_date
#row[0] + row[1] + row[2] + row[3] + row[4]row.id + row.tempvalue + row.tempdate 
