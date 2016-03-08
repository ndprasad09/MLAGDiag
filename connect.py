#!/usr/bin/python

import socket,os
import telnetlib
import sys
import getpass
import time
import re
import Library
import logging

#######################
#--- Global variables
#######################
global SwitchID_handlerdict
global switchInfo
SwitchID_handlerdict = {}
switchInfo = []
#########################################
#- Procedures
######################################

def Connect (host,username,password):
	"""
	This function establishes a telnet connection to the host
	and returns a connectionhandler object
	:param host: host ip address
	:param username: host username
	:param password: pasword
	:return: connectionhandler to the host
	"""
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


def ConnecttoSwitches():
    """
    This function will connect to multiple devices
	:return: a dctionary with keys as switch IDs and
			 values as connection handler object
    """
    global SwitchID_handlerdict
    switchIDList = []
    connHandler = []
    switchNum = raw_input("Please Enter Number of MLAG Switches to Debug: ")
    switchNum = int(switchNum)
    for eachSwitch in range(switchNum):
        tempSwitch = []
        eachSwitch = eachSwitch + 1
        while True:
            switchIP = raw_input('Please Enter IP Address of switch %d: ' % eachSwitch)
            try:
                socket.inet_aton(switchIP)
                break
            except socket.error:
                print "!!!IP address Entered is Invalid!!!"
                continue
        tempSwitch.append(eachSwitch)
        tempSwitch.append(switchIP)
        switchIDList.append(eachSwitch)
        switchInfo.append(tempSwitch)
        while True:
            username = raw_input('Please Enter UserName of Switch %d: ' % eachSwitch)
            # password = getpass.getpass (prompt = 'Enter your Password of Switch: ')
            password = raw_input('Please Enter Password of Switch %d: ' % eachSwitch)
            print "\n!!!Connecting to the Switch %d. Please Wait!!!" % eachSwitch

            retVal = Connect(switchIP, username, password)
            Library.SendCmd(retVal,"disable clipaging")
            if retVal == -1:
                continue
            elif retVal == -2:
                print "!!!Connection Timeout for Switch %d. Exiting the Script!!!" % eachSwitch
                sys.exit(1)
            else:
                connHandler.append(retVal)
                break
	SwitchID_handlerdict = dict(zip(switchIDList,connHandler))

def Closeconnectiontoswitches():
	"""
	Close all active telnet sessions
	:return:
	"""
	global SwitchID_handlerdict
	try:
		for keys in  SwitchID_handlerdict:
			SwitchID_handlerdict[keys].close()
			logging.info("Connection closed succesfully")
	except:
		logging.error("Could not close the connection !!!")
