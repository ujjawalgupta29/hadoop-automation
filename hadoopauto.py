#!/usr/bin/python36
import subprocess
import os 
import cgi

print("content-type: text/html\n")

form=cgi.FieldStorage()
mode=form.getvalue('cmd')
ip=form.getvalue('mip')
ruser=form.getvalue('user')
rip=form.getvalue('sip')
rpass=form.getvalue('pwd')
direc2=form.getvalue('fname')
#sys=input("enter where u want to set up hadoop(local/remote): ")
#ch=input("what u want to create master/slave: ")
#ip=input("enter master ip: ")

if mode=="ml":
	sys="local"
	ch="master"
elif mode=="mr":
	sys="remote"
	ch="master"
elif mode=="sl":
	sys="local"
	ch="slave"
elif mode=="sr":
	sys="remote"
	ch="slave"



if sys=="local":	
	
	if ch=="slave":
		
		#dir2=input("enter path of directory: ")
		#subprocess.getoutput("sudo mkdir /{}".format(dir2))	
		#print("go")
		f1=open('/var/www/html/hdfs-site.xml','w')
		f1.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.data.dir</name>
<value>/nn</value>
</property>

</configuration>""")
		f1.close()
		subprocess.getoutput("sudo cp /var/www/html/hdfs-site.xml /etc/hadoop/hdfs-site.xml")
		
		f2=open('/var/www/html/core-site.xml','w')
		f2.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))
		f2.close()
		subprocess.getoutput("sudo cp /var/www/html/core-site.xml /etc/hadoop/core-site.xml")
		
		subprocess.getoutput("sudo iptables -F")
		subprocess.getoutput("sudo setenforce 0")	
		
		subprocess.getoutput("sudo hadoop-daemon.sh start datanode")
		check=subprocess.getoutput("jps | grep DataNode")
		print(check)
		if(check==' '):
			print("Not running :(")
		else:
			print("Running :)")
		

	elif ch=="master":
		#dir1=input("enter name of directory: ")	
		f1=open('/var/www/html/hdfs-site.xml','w')
		f1.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.name.dir</name>
<value>/nn</value>
</property>

</configuration>""")
		f1.close()
		subprocess.getoutput("sudo cp /var/www/html/hdfs-site.xml /etc/hadoop/hdfs-site.xml")
		
		f2=open('/var/www/html/core-site.xml','w')
		f2.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))
		f2.close()
		
		subprocess.getoutput("sudo cp /var/www/html/core-site.xml /etc/hadoop/core-site.xml")
		#os.system("mkdir /{}".format(dir1))
		subprocess.getoutput("sudo setenforce 0")
		subprocess.getoutput("sudo iptables -F")
		subprocess.getoutput("sudo hadoop namenode -format -force")	
		subprocess.getoutput("sudo hadoop-daemon.sh start namenode")
		check=subprocess.getoutput("sudo jps | grep NameNode")
		print(check)		
		if(check==''):
			print("Not running :(")
		else:
			print("Running :)")

	


elif sys=="remote":
	

	if ch=="slave":
		
		subprocess.getoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l {} {} mkdir {}".format(rpass,ruser,rip,direc2))
		
		f1=open('/var/www/html/hdfs-site.xml','w')
		f1.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.data.dir</name>
<value>{}</value>
</property>

</configuration>""".format(direc2))
		f1.close()
		#print(direc2)
		
		f2=open('/var/www/html/core-site.xml','w')
		f2.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))
		f2.close()
		#print("or hua")

		subprocess.getoutput("sudo sshpass -p {} scp /var/www/html/hdfs-site.xml  {}@{}:/etc/hadoop/".format(rpass,ruser,rip))

		subprocess.getoutput("sudo sshpass -p {} scp  /var/www/html/core-site.xml  {}@{}:/etc/hadoop/".format(rpass,ruser,rip))
		#print("or hua")
		subprocess.getoutput("sudo sshpass -p {} ssh -l {} {} iptables -F".format(rpass,ruser,rip))	
			
		subprocess.getoutput("sudo sshpass -p {} ssh -l {} {} hadoop-daemon.sh start datanode".format(rpass,ruser,rip))
		#print("hello")
		#subprocess.getoutput("sudo rm /root/Desktop/hdfs-site.xml")
		#subprocess.getoutput("sudo rm /root/Desktop/core-site.xml")	
		check=subprocess.getoutput("sudo sshpass -p {} ssh -l {} {}  jps | grep DataNode".format(rpass,ruser,rip))
		if(check==''):
			print("Datanode Not running :(")
		else:
			print("Datanode Running :)")	
		
	
	
	elif ch=="master":
		#print("thoda or")
		subprocess.getoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l {} {} mkdir {}".format(rpass,ruser,ip,direc2))
		
		#dir1=input("enter path of directory: ")	
		f1=open('/var/www/html/hdfs-site.xml','w')
		f1.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.name.dir</name>
<value>{}</value>
</property>

</configuration>""".format(direc2))
		f1.close()
		
		f2=open('/var/www/html/core-site.xml','w')
		f2.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))
		f2.close()
		subprocess.getoutput("sudo sshpass -p {} scp /var/www/html/hdfs-site.xml  {}@{}:/etc/hadoop/".format(rpass,ruser,ip))
		
		subprocess.getoutput("sudo sshpass -p {} scp  /var/www/html/core-site.xml  {}@{}:/etc/hadoop/".format(rpass,ruser,ip))
		#print("thoda or")
		subprocess.getoutput("sudo sshpass -p {} ssh -l {} {} iptables -F".format(rpass,ruser,ip))	

		subprocess.getoutput("sudo sshpass -p {} ssh -l {} {} hadoop namenode -format -force ".format(rpass,ruser,ip))	
		subprocess.getoutput("sudo sshpass -p {} ssh -l {} {} hadoop-daemon.sh start namenode".format(rpass,ruser,ip))
		#print("thoda or")
		#subprocess.getoutput("rm /root/Desktop/hdfs-site.xml")
		#subprocess.getoutput("rm /root/Desktop/core-site.xml")
		check=subprocess.getoutput("sudo sshpass -p {} ssh -l {} {} jps | grep NameNode".format(rpass,ruser,ip))
		print(check)
		if(check==''):
			print("Namenode Not running :(")
		else:
			print("Namenode Running :)")
		

