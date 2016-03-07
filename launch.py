import MLAGSQL
import logging
import ValidationLib
import test

global c

# The default level is WARNING(30). The available levels are INFO(20),DEBUG(10),ERROR(40) and CRITICAL(50)
# Use the approppriate log levels for debug print outputs
logging.basicConfig(level=logging.ERROR)
logging.disable(logging.INFO)



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

MLAGSQL.AddMLAGPeerInstance(1,1,11,'sw2','VR-Default','51.2.2.1','two','51.2.2.2',2,'Up','None',1)
MLAGSQL.AddMLAGPeerInstance(1,2,12,'sw3','VR-Default','41.2.2.2','three','41.2.2.1',3,'Up','None',1)

MLAGSQL.AddMLAGPeerInstance(2,3,21,'sw1','VR-Default','51.2.2.2','two','51.2.2.1',2,'Up','None',2)
MLAGSQL.AddMLAGPeerInstance(2,4,22,'sw3','VR-Default','31.2.2.2','three','31.2.2.1',4,'Down','None',1)

MLAGSQL.AddMLAGPeerInstance(3,5,31,'sw1','VR-Default','41.2.2.1','two','41.2.2.2',3,'Up','MD5',1)
MLAGSQL.AddMLAGPeerInstance(3,6,32,'sw2','VR-Default','31.2.2.1','three','31.2.2.2',4,'Up','None',1)

ValidationLib.CheckMLAGStatus()


# AddPortInstance
#  (SwitchID integer,ISCID integer,PortID Text,MLAGID integer,  VlanName Text,VlanTag integer,Tagged integer, PRIMARY KEY(SwitchID,VlanTag)
MLAGSQL.AddPortInfo(1,1,'2:10',7,'v3',3,1)
MLAGSQL.AddPortInfo(1,1,'2:21',0,'v3',3,0)
MLAGSQL.AddPortInfo(1,1,'3:11',7,'v4',4,1)
MLAGSQL.AddPortInfo(1,1,'52',8,'v5',5,1)
MLAGSQL.AddPortInfo(1,1,'52',9,'v6',6,1)
MLAGSQL.AddPortInfo(1,1,'52',100,'v100',4095,0)


Switch1="1"
test.VlanCheck(Switch1)


#Debug functions to see  table content
MLAGSQL.DebugShowMLAGTable()
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