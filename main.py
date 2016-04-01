#!/usr/bin/python

import MLAGSQL
import logging
import connect
import MLAGPeer
import MLAGPorts
import ValidationLib
import vLanCheck
import interVLANCheck
import argparse
import socket
import sys
import Library

# The default level is WARNING(30). The available levels are INFO(20),DEBUG(10),ERROR(40) and CRITICAL(50)
# Use the approppriate log levels for debug print outputs
logging.basicConfig(level=logging.INFO)
#logging.disable(logging.INFO)
logging.disable(logging.ERROR)


"""
-> Connect to DB and create Tables
-> Connect to the Switches and return handler
"""

#Adding Disclaimer
print ("DISCLAIMER:")
print ("This Program is to diagnose the MLAG Configuration between peers")
print ("This Program does not make any changes to any switch configuration")
print ("It is free software and it comes without any Warranty")
print ("\n")

# Function Calls to populate the Database
"""
-> Function Calls to fetch and populate the Database
AddMlagPeerInstance
AddMlagPortInstance
"""

parser = argparse.ArgumentParser(description='mLAG Diag tool to diagnose misconfig across mlag peers')
parser.add_argument('-n', action="store", dest='peers', default=None, help='Enter number of peers in the network')
parser.add_argument('-c', action="store", dest='connect', nargs="+", default=None, help='Host IP in the format user:pass@host1 user:pass@host2')
args = parser.parse_args()
switchNum=args.peers
switchIpList=args.connect

if switchNum and switchIpList != None:
    # Connect to the Database
    MLAGSQL.ConnectDatabase()

    #Create the tables required for analysis
    MLAGSQL.CreateTables()
    connect.cliparser(switchNum,switchIpList)
else:

    # Connect to the Database
    MLAGSQL.ConnectDatabase()

    #Create the tables required for analysis
    MLAGSQL.CreateTables()
    connect.ConnecttoSwitches()
# Connect to the switches

#connect.ConnecttoSwitches()
SwitchID_handler=connect.SwitchID_handlerdict
#SwitchID_handler=SwitchID_handlerdict

for key in SwitchID_handler:
#-- AddMLAGPeerInstance - Population of MLag Peer ISC Vlan details in the MLAG Peer table
    MLAGPeer.get_mlag_peer(SwitchID_handler[key],key)
    MLAGSQL.DebugShowMLAGTable()



#--ISIC Replace call from Validation Library - To unify the ISC ID across switches
ValidationLib.replaceISCID()


MLAGSQL.DebugShowMLAGTable()


#-- AddMLAGPortInstance - Population of Port- Vlan Information in the PortInfo Table
for key in SwitchID_handler:
    MLAGPorts.MlagPort(SwitchID_handler[key],key)


MLAGSQL.DebugShowPortTable()

connect.Closeconnectiontoswitches()



#--- Calling CheckMLAGStatus()
ValidationLib.CheckMLAGStatus()


#Debug functions to see table content
"""
-> Function calls for MLAG data validation
CheckMLAG
CheckVLAN
Check Inter Vlan
"""


#--- Calling VlanCheck()
vLanCheck.VlanCheck()

#---- Calling interVLANCheck()
interVLANCheck.interVLANCheck()

#---- Print the table contents
MLAGSQL.DebugShowPortTable()

"""
-> Cleanup and Close
"""

#Delete all the tables
MLAGSQL.DeleteTables()

#Disconnect the database
MLAGSQL.CloseDatabase()

print ("\nDiag Completed!")
