#coding=utf-8 
'''
Created on Aug 24, 2012

@author: yang_sen
'''
import sys
import os

try:
    import MySQLdb
except Exception,e:
    print e  
    print "You don't have MySQLdb Modual"
    print "Error,force quit"
    sys.exit(1) 


'''
'执行sql语句
'''  
def execSQL(cursor,sqlstr):
    try:
        cursor.execute(sqlstr)
    except Exception,e:
        print e 
        print "SQL execute Error,force quit"
        sys.exit(1)



'''
'程序主体开始
'''  
        
#读取配置文件循环，将host dbname等弄个数组
if not os.path.exists("autoInstall.txt"):
    print "Can't find autoInstall.txt in current path. Error,force quit" 
    sys.exit(1)
    
#定义参数列表
list_master_host=[]
list_master_user=[]
list_master_password=[]
list_master_port=[]
list_DB_name=[]
list_fullSchemaSqlFilePath=[]
list_upgradeSchemaSqlFilePath=[]
list_sockPath=[]

#从文件中取出参数放入各个列表    
try:
    fileHandle = open('autoInstall.txt','r')  
    for line in fileHandle:
        try:
            if line[0:1]=='#' or  line[0:2]=='//':
                continue 
            nPos = line.index('=')
            parameter=str(line.split('=',1)[1][:-1]).strip()
            if line.split('=',1)[0]=='master_host':
                list_master_host.append(parameter)
            elif line.split('=',1)[0]=='master_user':
                list_master_user.append(parameter)
            elif line.split('=',1)[0]=='master_password':
                list_master_password.append(parameter)
            elif line.split('=',1)[0]=='master_port':
                list_master_port.append(parameter)
            elif line.split('=',1)[0]=='DB_name':
                list_DB_name.append(parameter)
            elif line.split('=',1)[0]=='fullSchemaSqlFilePath':
                list_fullSchemaSqlFilePath.append(parameter)
            elif line.split('=',1)[0]=='upgradeSchemaSqlFilePath':
                list_upgradeSchemaSqlFilePath.append(parameter)
            elif line.split('=',1)[0]=='sockPath':
                list_sockPath.append(parameter)
           
        except Exception,e:
            continue
       
    
    fileHandle.close()  
         
except Exception,e:
    print e 
    print "Error,force quit" 
    sys.exit(1)
    
#判断文件中是否缺少配置了某项
hostNumber=list_master_host.__len__()
if( list_master_user.__len__()!=hostNumber  or
     list_master_password.__len__()!=hostNumber  or
     list_master_port.__len__()!=hostNumber  or
     list_DB_name.__len__()!=hostNumber  or
     list_fullSchemaSqlFilePath.__len__()!=hostNumber or
     list_upgradeSchemaSqlFilePath.__len__()!=hostNumber or
     list_sockPath.__len__()!=hostNumber):
    print "please check autoInstall.txt. Error,force quit"
    sys.exit(1)
    
    
content = raw_input("Are you sure to drop the databases ? your choice(Y/N):")
if content!='Y' and content!='y':
    sys.exit(1)
    
#配置各个host的主循环体开始

count=0
while count<hostNumber:
    
    #配置当前这次循环的host参数
    master_host=list_master_host[count]
    master_user=list_master_user[count]
    master_password=list_master_password[count]
    master_port=int(list_master_port[count])
    DB_name=list_DB_name[count]
    fullSchemaSqlFilePath=list_fullSchemaSqlFilePath[count]
    upgradeSchemaSqlFilePath=list_upgradeSchemaSqlFilePath[count]
    sockPath=list_sockPath[count]
    
    count+=1
    print "\nBegin "+str(count)+"th host"
    
    try: 
        #连接数据库
        if os.path.exists(sockPath): 
            connection = MySQLdb.connect(user=master_user,passwd=master_password,host=master_host,port=master_port,charset='utf8',unix_socket=sockPath)
        else:
            connection = MySQLdb.connect(user=master_user,passwd=master_password,host=master_host,port=master_port,charset='utf8')
       
        cursor = connection.cursor()
        
    except Exception,e:
        print e 
        print "Error,force quit"  
        sys.exit(1)
  
    execSQL(cursor,"drop database if exists "+DB_name+";")
    
    try: 
        cursor.close()
        connection.close()
    except Exception,e:
        print e 
        sys.exit(1)

print '\nAll finished!'