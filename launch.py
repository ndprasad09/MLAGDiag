import MLAGSQL
import logging
import connect
import MLAGPeer
import MLAGPorts
# The default level is WARNING(30). The available levels are INFO(20),DEBUG(10),ERROR(40) and CRITICAL(50)
# Use the approppriate log levels for debug print outputs
logging.basicConfig(level=logging.INFO)

# Connect to the Database
MLAGSQL.ConnectDatabase()

logging.info("Testing")

#Create the tables required for analysis
MLAGSQL.CreateTables()

# Add the following Procs
# AddMlagPeerInstance

#(SwitchID integer,ISCID integer,ISCPort integer,
# MLAGPeerName text,VRName text,PeerIPAddress text,
# ISCVlanName text,ISCIP text,ISCVlanTag int,ChkPtStatus int,
# AuthMethod text,NumMLAGPorts int,PRIMARY KEY(SwitchID,ISCID))")

# Connect to the switches

connect.ConnecttoSwitches()
SwitchID_handler=connect.SwitchID_handlerdict
for key in SwitchID_handler:
    #-- AddMLAGPeerInstance
    MLAGPeer.get_mlag_peer(SwitchID_handler[key],key)
    MLAGSQL.DebugShowMLAGTable()
    MLAGPorts.MlagPort(SwitchID_handler[key],key)
    #-- AddPortInstance
connect.Closeconnectiontoswitches()
#MLAGSQL.AddMLAGPeerInstance(1,1,11,'sw1','VR-Default',PeerIPAddress,ISCVlan,LocalIPAddress,2,'Up','None',1)



# AddPortInstance
#  (SwitchID integer,ISCID integer,PortID integer,MLAGID integer,  VlanName Text,VlanTag integer,Tagged integer, PRIMARY KEY(SwitchID,VlanTag)


#Debug functions to see  table content

MLAGSQL.DebugShowPortTable()

#Loading the Tables
# PArse the customer data and get connection detail for each switch
# Connect to each switch. For each switch, - DUrga
# Get the MLAG Peer and MLAG port info and load the MLAGPeer Table - Ramesh
# Get list of ports from the show MLAG port command
# For each port in the list get the associated vlan Information - Name,tag,Link State etc.
# For ISC port get the associated Vlan Information and load it into the DB

#Notes : Looks like there will be a flag needed in PortInfo for quick look up of associated VLans
#Validation Functions
#GetList of all MLAG Ports for a given MLAGID in a Switch
#for each Mlag Port get a list of associated Vlan tags
#Get list of Vlan tags for the ISC Vlan
#Check if each tag is represented in the ISC Vlan

# GetMLAGParameters
# Get specific parameters from the MLAG table needed like ISC VLan name / Tag , ISC IP ,Auth Method etc.

#Delete all the tables
MLAGSQL.DeleteTables()

#Disconnect the database
MLAGSQL.CloseDatabase()