import MLAGSQL
import logging

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
MLAGSQL.AddMLAGPeerInstance(1,7,'sw2','VR-Default','51.2.2.1','two','51.2.2.2',2,'Up','None',1)
MLAGSQL.AddMLAGPeerInstance(2,17,'sw2','VR-Default','51.2.2.2','two','51.2.2.1',2,'Up','None',1)

# AddPortInstance
MLAGSQL.AddPortInfo(1,52,7,'Enabled','Active','v3',3,1)

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