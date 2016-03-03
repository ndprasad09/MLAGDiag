#!/usr/bin/python

import socket,os
import telnetlib
import sys
import getpass
import time
import re

global sHandler
global timeout
global IPAddress 
global username
global password

sHandler = 0
timeout = 5



#########################################
#- Procedures
######################################



def Connect ():

	global sHandler

	IPAddress = raw_input ("\nPlease Enter your Management IP Address: ")
	try:
		socket.inet_aton(IPAddress)
	except socket.error:
		print "\n!!! Error: Please Enter Valid IP Address !!!\n"
		sys.exit()

	username = raw_input("Enter your Username: ")
	password = raw_input("Enter your Password: ")

	try:
		if sHandler == 0:
			sHandler = telnetlib.Telnet (IPAddress) 

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
			
	except socket.timeout:
		print "\nNo Connection to your Host: "+host+"\n" 
		sys.exit() 


	


