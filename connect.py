#!/usr/bin/python

import socket, os
import telnetlib
import sys
import getpass
import time
import re
import Library
import logging

#######################
# --- Global variables
#######################
global SwitchID_handlerdict
global SwitchID_switchInfo
SwitchID_handlerdict = {}
SwitchID_switchInfo = {}
#########################################
# - Procedures
######################################

def Connect(host, username, password):
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
            sHandler = telnetlib.Telnet(host)

            print ("\nConnecting in 3 Seconds")
            for i in range(3):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1)

            sHandler.read_until("login")
            sHandler.write(username + "\n")
            sHandler.read_until("password")
            sHandler.write(password + "\n")
            retIndex, retObj, retStr = sHandler.expect(['.*#', 'incorrect'])

            if retIndex == 1:
                print ("\n!!! Error: InValid Credentials !!!\n")
                return -1

            else:
                print "\n!!!!Connection Successfull!!!\n"
            # prompt=re.compile(r'.\d+\s[#>]\s$')
            # sHandler.expect ([prompt])
            # SendCmd ("disable clip")
            return sHandler

    except socket.timeout:
        print ("\nNo Connection to your Host: " + host + "\n")
        sys.exit()
    except socket.error:
        print ("\n Connection attempt Failed. Please check your Connectivity")
        sys.exit()


def ConnecttoSwitches():
    """
    This function will connect to multiple devices
    :return: a dctionary with keys as switch IDs and
             values as connection handler object
    """
    global SwitchID_handlerdict
    global SwitchID_switchInfo
    switchInfo = []
    switchIDList = []
    switchIPList = []
    connHandler = []
    switchNum = raw_input("Please Enter Number of MLAG Switches to Debug: ")
    switchNum = int(switchNum)
    for eachSwitch in range(switchNum):
        Flag = 0
        tempSwitch = []
        eachSwitch = eachSwitch + 1
        while True:
            switchIP = raw_input('Please Enter IP Address of switch %d: ' % eachSwitch)

            try:
                socket.inet_aton(switchIP)

            except socket.error:
                print "!!!IP address Entered is Invalid!!!"
                continue
            else:

                for eachItem in switchInfo:
                    if switchIP == eachItem[1]:
                        print (
                            "IP address is already Entered for Switch %d. Please Enter IP address of Switch %d" % (
                            eachItem[0], eachSwitch))
                        Flag = 1
                        break
                if Flag == 1:
                    Flag = 0 #Resetting the Flag
                    continue
                else:
                    tempSwitch.append(eachSwitch)
                    tempSwitch.append(switchIP)
                    switchIDList.append(eachSwitch)
                    switchInfo.append(tempSwitch)
                    break




        while True:
            username = raw_input('Please Enter UserName of Switch %d: ' % eachSwitch)
            # password = getpass.getpass (prompt = 'Enter your Password of Switch: ')
            password = raw_input('Please Enter Password of Switch %d: ' % eachSwitch)
            print "\n!!!Connecting to the Switch %d. Please Wait!!!" % eachSwitch

            retVal = Connect(switchIP, username, password)
            Library.SendCmd(retVal, "disable clipaging")
            if retVal == -1:
                continue
            elif retVal == -2:
                print "!!!Connection Timeout for Switch %d. Exiting the Script!!!" % eachSwitch
                sys.exit(1)
            else:
                connHandler.append(retVal)
                break
        SwitchID_handlerdict = dict(zip(switchIDList, connHandler))
        SwitchID_switchInfo = dict(zip(switchIDList,switchInfo))
        GetSwitchInfo()


def Closeconnectiontoswitches():
    """
    Close all active telnet sessions
    :return:
    """
    global SwitchID_handlerdict
    try:
        for keys in SwitchID_handlerdict:
            SwitchID_handlerdict[keys].close()
            logging.info("Connection closed succesfully")
    except:
        logging.error("Could not close the connection !!!")

def GetSwitchInfo():
    """
    This function gets switch specific information
    :return:
    """

    global SwitchID_switchInfo
    global SwitchID_handlerdict

    for switchid in SwitchID_handlerdict:
        switchinfo = []
        SwitchIP=SwitchID_switchInfo[switchid][1]
        retString = Library.SendCmd(SwitchID_handlerdict[switchid],"show switch")
        match = re.search(r'System\s+MAC:\s+(.*)\n',retString)
        if match:
             SwitchMAC = match.groups(1)[0].strip('\r')
        else :
            SwitchMAC = "UNKnown"
        SwitchID_switchInfo[switchid].extend(SwitchMAC)
        match = re.search(r'SysName:\s+(.*)\n',retString)
        if match:
             SwitchName = match.groups(1)[0].strip('\r')
        else :
            SwitchName = "UNKnown"

        switchinfo.append(SwitchIP)
        switchinfo.append(SwitchMAC)
        switchinfo.append(SwitchName)
        SwitchID_switchInfo[switchid] = list(switchinfo)
def DisplaySwitchInfo(switchID):
    """
    Display the switch specific info for switch ID
    :return:
    """
    global SwitchID_switchInfo
    global SwitchID_handlerdict
    print ("\tSwitch Name:  "+str(SwitchID_switchInfo[switchID][2]))
    print ("\tSwitch IP:  "+str(SwitchID_switchInfo[switchID][0]))
    print ("\tSwitch MAC:  "+str(SwitchID_switchInfo[switchID][1]))
