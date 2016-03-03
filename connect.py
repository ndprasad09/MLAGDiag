#!/usr/bin/python

import socket,os
import telnetlib
import sys
import getpass
import time
import re




#########################################
#- Procedures
######################################



def Connect (host,username,password):

	#global sHandler


	sHandler = 0
	try:
		if sHandler == 0:
			sHandler = telnetlib.Telnet (host)

			print "\nConnecting in 3 Seconds"
			for i in range(3):
				print ".",
				sys.stdout.flush()
				time.sleep(1)

			sHandler.read_until("login")
			sHandler.write (username + "\n")
			sHandler.read_until("password")
			sHandler.write(password + "\n") 
			retIndex,retObj, retStr= sHandler.expect (['.*#','incorrect'])

			if retIndex == 1:
				print "\n!!! Error: InValid Credentials !!!\n"
				sys.exit() 

			else:
				print "\n Connection Successfull \n"
			#prompt=re.compile(r'.\d+\s[#>]\s$')
			#sHandler.expect ([prompt])
			#SendCmd ("disable clip")
			return sHandler
			
	except socket.timeout:
		print "\nNo Connection to your Host: "+host+"\n" 
		sys.exit() 


	


