import logging
import MLAGSQL
import ValidationLib
import vLanCheck
import interVLANCheck




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

MLAGSQL.AddMLAGPeerInstance(1,1,11,'sw2','VR-Default','51.2.2.1','two','51.2.2.2',2,'Up','None',1)
MLAGSQL.AddMLAGPeerInstance(1,2,12,'sw3','VR-Default','41.2.2.2','three','41.2.2.1',3,'Up','None',1)

MLAGSQL.AddMLAGPeerInstance(2,1,21,'sw1','VR-Default','51.2.2.2','two','51.2.2.1',2,'Up','None',1)
MLAGSQL.AddMLAGPeerInstance(2,2,22,'sw3','VR-Default','31.2.2.2','three','31.2.2.1',4,'Up','None',1)

MLAGSQL.AddMLAGPeerInstance(3,1,31,'sw1','VR-Default','41.2.2.1','two','41.2.2.2',2,'Up','None',1)
MLAGSQL.AddMLAGPeerInstance(3,2,32,'sw2','VR-Default','31.2.2.1','three','31.2.2.2',4,'Up','None',1)


# AddPortInstance
#  (SwitchID integer,ISCID integer,PortID integer,MLAGID integer,  VlanName Text,VlanTag integer,Tagged integer, PRIMARY KEY(SwitchID,VlanTag)
MLAGSQL.AddPortInfo(1,1,52,7,'v3',3,1)
MLAGSQL.AddPortInfo(1,1,52,7,'v4',4,1)
MLAGSQL.AddPortInfo(1,1,52,8,'v5',5,1)
MLAGSQL.AddPortInfo(1,1,52,9,'v6',6,1)
MLAGSQL.AddPortInfo(1,1,52,100,'v100',4095,0)
MLAGSQL.AddPortInfo(2,1,52,7,'v3',3,0)
MLAGSQL.AddPortInfo(2,1,52,7,'v4',101,1)


#--- Calling CheckMLAGStatus()

ValidationLib.CheckMLAGStatus()

#--- Calling VlanCheck()

vLanCheck.VlanCheck()

#---- Calling interVLANCheck()

interVLANCheck.interVLANCheck()


#Delete all the tables
MLAGSQL.DeleteTables()

#Disconnect the database
MLAGSQL.CloseDatabase()
