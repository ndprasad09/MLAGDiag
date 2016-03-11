import MLAGSQL
import logging
import connect
import MLAGPeer
import MLAGPorts
import ValidationLib
import vLanCheck
import interVLANCheck
# The default level is WARNING(30). The available levels are INFO(20),DEBUG(10),ERROR(40) and CRITICAL(50)
# Use the approppriate log levels for debug print outputs
logging.basicConfig(level=logging.INFO)

"""
-> Connect to DB and create Tables
-> Connect to the Switches and return handler
"""
# Connect to the Database
MLAGSQL.ConnectDatabase()

#Create the tables required for analysis
MLAGSQL.CreateTables()

# Function Calls to populate the Database
"""
-> Function Calls to fetch and populate the Database
AddMlagPeerInstance
AddMlagPortInstance
"""
# Connect to the switches
connect.ConnecttoSwitches()
SwitchID_handler=connect.SwitchID_handlerdict

for key in SwitchID_handler:
#-- AddMLAGPeerInstance - Population of MLag Peer ISC Vlan details in the MLAG Peer table
    MLAGPeer.get_mlag_peer(SwitchID_handler[key],key)
    MLAGSQL.DebugShowMLAGTable()

#--ISIC Replace call from Validation Library - To unify the ISC ID across switches
ValidationLib.replaceISCID()

#-- AddMLAGPortInstance - Population of Port- Vlan Information in the PortInfo Table
for key in SwitchID_handler:
    MLAGPorts.MlagPort(SwitchID_handler[key],key)
    MLAGSQL.DebugShowPortTable()

connect.Closeconnectiontoswitches()

#Debug functions to see table content
"""
-> Function calls for MLAG data validation
CheckMLAG
CheckVLAN
Check Inter Vlan
"""
#--- Calling CheckMLAGStatus()
ValidationLib.CheckMLAGStatus()

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
