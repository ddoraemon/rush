[概述]：
	本脚本是 DB自动化安装脚本。     
	
[依赖库]：
	python python-mysqldb 请先运行aptitude install python python-mysqldb 确保Python及python-mysqldb模块已安装
	
[配置文件]：
    

首先配置你的mysql交互程序所在路径

1. 每个服务器有11项配置（删除任何一项将无法运行！密码前后不能有空格，会被忽略）：
master_host表示mysql host的IP
master_user=mysql的用户名 （注：此处必须是能有create database create table及赋权等 权限的超级用户）
master_password=mysql的用户密码
master_port=mysql的端口号
sockPath=mysql.sock所在的路径 （注：使用ps aux|grep mysql 可以看到类似--socket=/tmp/mysqld.sock /tmp/mysqld.sock 即为sockPath）
DB_name=mysql的连接时要设置的数据库名
fullSchemaSqlFilePath=全新安装的sql文件的路径
upgradeSchemaSqlFilePath=升级的sql文件的路径
app_user=应用程序连接mysql所用帐号
app_password=应用程序连接mysql所用密码
allowHosts=该数据库允许连接的IP（%是通配符）

配置示例：
master_host=192.168.40.203
master_user=root
master_password=123
master_port=3306
sockPath=/tmp/mysqld.sock
DB_name=trace_log
fullSchemaSqlFilePath=./vddb5.2.3fulldbschema/trace_log.sql
upgradeSchemaSqlFilePath=
app_user=vdna4x
app_password=123456
allowHosts=192.168.40.%

2.配置文件中不能出现单引号，双引号，等号
3.路径支持相对路径和绝对路径(比如 ‘/home/ys/Desktop/a1.sql‘ 或者 ‘./tt/a1.sql‘ 或者 ‘a1.sql‘都是合法的)。
4.程序不支持～这个路径，需要写全，比如 ‘/home/ys/test.sql‘
5.配置文件中可以配置多台host，但是必须保证每个host都有11项配置，脚本会按照配置文件的顺序进行
6.如果没有密码，可以将master_password等号后面设置为空，但不能删除master_password这个配置项。
7.如果本次安装不需要授权，请将app_user或者app_password或者allowHosts设置为空，但不能删除这些配置项
8.#或者//注释一行，注意本脚本不支持在某个配置项的后面追加注释，所以注释请务必另起一行 ！
9.配置文件必须和脚本放在同一目录.
10.如果是配置本机，一般需要配置本机的mysql.sock所在路径；配置远程的主机需将sockPath设置为空（但不能删除该配置项）


[注意点]：
1.运行该脚本的机子需要拥有远程数据库的登录、create、index、drop、alter的权限
2.一个sql文件中只能对一个数据库进行操作，并且不用写use语句，只需要配置DB_name项。多个数据库可以通过配置多个配置选项来实现。
3 创建有赋权的超级用户示例：grant all on *.* to 'root'@'192.168.40.20' identified by '123' with grant option; 


执行步骤：
1 配置好autoinstall.txt，注意权限 DB名称 脚本路径等
2 python autoInstall.py


