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
'导入Schema的SQL文件，不使用事务
'''  
def sourceSqlFile(SqlFilePath,cursor,host,user,password,dbname,sockPath,mysqlpath):
    try:    
        if SqlFilePath[0:1]!="/":
            SqlFilePath=os.path.abspath(SqlFilePath)
            
        if not os.path.exists(SqlFilePath):
            print "Can't find sql file，please check the autoInstall.txt. Error,force quit" 
            sys.exit(1)
            
        print "Start ["+host+"]:"+dbname
        
       
        if password=='':
            if os.path.exists(sockPath): 
                os.popen(mysqlpath+" -h"+host+" -u"+user+" --database="+dbname+" --socket="+sockPath+"<"+SqlFilePath+" 2>err.log")
            else:
                os.popen(mysqlpath+" -h"+host+" -u"+user+" --database="+dbname+" <"+SqlFilePath+" 2>err.log")
    
        else:
            if os.path.exists(sockPath):                
                os.popen("mysql -h"+host+" -u"+user+" -p"+password+" --database="+dbname+" --socket="+sockPath+"<"+SqlFilePath+" 2>err.log")
            else:
                os.popen("mysql -h"+host+" -u"+user+" -p"+password+" --database="+dbname+" <"+SqlFilePath +" 2>err.log")
        
        
        if not os.path.exists(os.path.abspath('err.log')):
            return 1
        
        try: 
            errFileHandle = open('err.log','r')  
            strinfo=errFileHandle.read()
        except Exception,e:
            print e  
            print "Read errorlog error，force quit" 
            sys.exit(1)
            
        if(strinfo.find('ERROR')!=-1):
            print strinfo
            try:
                errFileHandle.close()
            except Exception,e:
                print e
                print "Close errorlog error，force quit"
                sys.exit(1) 
            return 0
        else:
            try:
                errFileHandle.close()
            except Exception,e:
                print e
                print "Close errorlog error，force quit"
                sys.exit(1) 
            return 1
        
        print "Finish ["+host+"]:"+dbname          
    except Exception,e:
        print e  
        print "Error，force quit" 
        sys.exit(1)

  
'''
'检查用户是否有创建的权限
'''   
def checkPrivilege(cursor,user):
    try:    
        #print "checkPrivilege "
        execSQL(cursor,"use mysql;")
       
        sqlstr="select Create_priv from user where Create_priv='Y' and Index_priv='Y' and Alter_priv='Y' and Drop_priv='Y' and User='"+user+"';"
        cursor.execute(sqlstr)
        if cursor.rowcount<=0:
            print "This user does not have create,drop,alter,index privilege. Error,force quit" 
            sys.exit(1)   
                
        #print "This user has create,drop,alter,index privilege"          
    except Exception,e:
        print e  
        print "This user does not have create,drop,alter,index privilege. Error,force quit "
        sys.exit(1) 
        
'''
'打印权限
'''              
def printPrivilege(SqlFilePath,dbname):
    try: 
        if SqlFilePath[0:1]!="/":
            SqlFilePath=os.path.abspath(SqlFilePath) 
        fileHandle = open(SqlFilePath,'r')  
        for line in fileHandle: 
            oldline=line.strip()
            line=line.strip().upper()    
            if line.find('GRANT')!=-1 and line.find('ON')!=-1 and line.find('TO')!=-1:
                print "ON DB [ "+dbname+" ] : " +oldline[line.find(' TO '):]  
        fileHandle.close()    
    except Exception,e:
        print e  
        sys.exit(1)   
           
  
'''
'程序主体开始
'''          
#读取配置文件循环，将host dbname等弄个数组
if not os.path.exists("autoInstall.txt"):
    print "Can't find autoInstall.txt in current path. Error,force quit " 
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
list_app_user=[]
list_app_password=[]
list_allowHosts=[]


mysqlpath=''

#从文件中取出参数放入各个列表    
try:
    fileHandle = open('autoInstall.txt','r')  
    for line in fileHandle:
        try:
            if line[0:1]=='#' or  line[0:2]=='//':
                continue 
            nPos = line.index('=')
            parameter=str(line.split('=',1)[1][:-1]).strip()
            if line.split('=',1)[0]=='mysqlpath':
                mysqlpath=parameter
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
            elif line.split('=',1)[0]=='app_user':
                list_app_user.append(parameter)
            elif line.split('=',1)[0]=='app_password':
                list_app_password.append(parameter)
            elif line.split('=',1)[0]=='allowHosts':
                list_allowHosts.append(parameter)    
                
                
           
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
     list_sockPath.__len__()!=hostNumber or
     list_app_user.__len__()!=hostNumber or
     list_app_password.__len__()!=hostNumber or
     list_allowHosts.__len__()!=hostNumber ):
    print "please check 'autoInstall.txt',make sure every host has 8 parameters. Error,force quit"
    sys.exit(1)

    

print "Start checking the parameters in the file 'autoIntall.txt'"

#检查sql文件是否存在

for sqlfile in list_fullSchemaSqlFilePath:
    if sqlfile=='':
        continue;
    if not os.path.exists(os.path.abspath(sqlfile)):
        print "Can't find the sql file [ "+sqlfile+" ] . Error,force quit"
        sys.exit(1)
            

for sqlfile in list_upgradeSchemaSqlFilePath:
    if sqlfile=='':
        continue;
    if not os.path.exists(os.path.abspath(sqlfile)):
        print "Can't find the sql file [ "+sqlfile+" ] . Error,force quit"
        sys.exit(1)

    
#判断是否存在mysql目录
if not os.path.exists(mysqlpath):
    print "Can't find mysql ，Error,force quit" 
    sys.exit(1)    



#检查是否每个host可以连接
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
    
    if fullSchemaSqlFilePath!='' and upgradeSchemaSqlFilePath!='':
        print "fullSchemaSqlFilePath and upgradeSchemaSqlFilePath must have one be empty. Error,force quit"  
        sys.exit(1)
    
    try: 
        #连接数据库
        if os.path.exists(sockPath): 
            connection = MySQLdb.connect(user=master_user,passwd=master_password,host=master_host,port=master_port,charset='utf8',unix_socket=sockPath)
        else:
            connection = MySQLdb.connect(user=master_user,passwd=master_password,host=master_host,port=master_port,charset='utf8')
       
        cursor = connection.cursor()
    except Exception,e:
        print e 
        print "Connect to "+master_user+" @ [ "+master_host+" ] ,please check the parameters. Error,force quit"  
        sys.exit(1)
    
    #检查用户是否有创建的权限
    checkPrivilege(cursor,master_user)
    try: 
        cursor.close()
        connection.close()
    except Exception,e:
        print e 
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
    app_user=list_app_user[count]
    app_password=list_app_password[count]
    allowHosts=list_allowHosts[count]
    
    
    count+=1
    print "\nBegin "+str(count)+"th host"
    
    if fullSchemaSqlFilePath=='' and upgradeSchemaSqlFilePath=='':
        print "fullSchemaSqlFilePath and upgradeSchemaSqlFilePath are both empty, skip"
        continue;
    
    try: 
        #连接数据库
        if os.path.exists(sockPath): 
            connection = MySQLdb.connect(user=master_user,passwd=master_password,host=master_host,port=master_port,charset='utf8',unix_socket=sockPath)
        else:
            connection = MySQLdb.connect(user=master_user,passwd=master_password,host=master_host,port=master_port,charset='utf8')
       
        cursor = connection.cursor()
    except Exception,e:
        print e 
        print "Connect to mysql error,please check the parameters. Error,force quit"  
        sys.exit(1)
    
    #授权
    if(app_user!='' and app_password!='' and allowHosts!=''):
        execSQL(cursor,"GRANT SELECT, INSERT, UPDATE, DELETE ON "+DB_name+".* TO '"+app_user+"'@'"+allowHosts+"' IDENTIFIED BY '"+app_password+"';")
    

    if fullSchemaSqlFilePath=='':
        content='u'
    elif upgradeSchemaSqlFilePath=='':
        content='f'
    
    isok=1  
    if  content=='f': #full安装
        #如果没有这个DB_name，创建数据库    
        execSQL(cursor,"create database "+DB_name+";")
        #导入full的sql文件
        isok=sourceSqlFile(fullSchemaSqlFilePath,cursor,master_host,master_user,master_password,DB_name,sockPath,mysqlpath)
   
    elif content=='u':   #upgrade
        #导入upgrade的sql文件
        isok=sourceSqlFile(upgradeSchemaSqlFilePath,cursor,master_host,master_user,master_password,DB_name,sockPath,mysqlpath)
    
    if isok==0:
        print "Source sqlFile Error,force quit"  
        sys.exit(1)
    
    #打印权限
#    if content=='F' or content=='f': #full安装
#        printPrivilege(fullSchemaSqlFilePath,DB_name)
#   
#    elif content=='U' or content=='u':   #upgrade
#        printPrivilege(upgradeSchemaSqlFilePath,DB_name)
    
    
    try: 
        cursor.close()
        connection.close()
    except Exception,e:
        print e 
        sys.exit(1)
        
print '\nAll finished!'
