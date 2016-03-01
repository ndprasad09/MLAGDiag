import sqlite3
import logging

########################################################
# Global Variables
#########################################################
global conn
global c

########################################################################################################################
# Member functions
########################################################################################################################
# def ConnectDatabase():
# def CreateTables():
# def AddMLAGPeerInstance(MLAGID,MLAGPeerName,VRName,LocalIPAddress,ISCVlanName,ISCIP,ISCVlanTag,ChkPtStatus,AuthMethod,NumMLAGPorts):
# def AddPortInfo(PortID,MLAGID,AdminState,LinkState,VlanName,VlanTag,Tagged):
# def DebugShowMLAGTable():
# def DebugShowPortTable():
# def DeleteTables():
# def CloseDatabase():
########################################################################################################################

def ConnectDatabase():
    """
    Connect to the SQLite Database
    """
    global conn
    global c
    conn = sqlite3.connect('mlag.db',timeout=2)

    c = conn.cursor()


def CreateTables():
    """
    Create the two databases :
    MLAGPeer - contains the global MLAG variables
    PortInfo - contains the information specific to the port
    :return:
    """
    global conn
    global c
    # Create Table

    #Check if stale table MLAGPeer exists before Creating the new one
    result = c.execute("PRAGMA table_info(MLAGPeer)")
    Complete = result.fetchall()
    if len(Complete) != 0:
        c.execute("drop table MLAGPeer")
        logging.debug("The table MLAGPeer exists and is deleted")
    c.execute(
    "CREATE TABLE MLAGPeer (SwitchID integer,ISCID integer,ISCPort integer,MLAGPeerName text,VRName text,PeerIPAddress text,ISCVlanName text,ISCIP text,ISCVlanTag int,ChkPtStatus int,AuthMethod text,NumMLAGPorts int,PRIMARY KEY(SwitchID,ISCID))")

    #Check if stale table PortInfo exists before Creating the new one
    result = c.execute("PRAGMA table_info(PortInfo)")
    Complete = result.fetchall()
    if len(Complete) != 0:
        c.execute("drop table PortInfo")
        logging.debug("The table PortInfo exists and is deleted")

    c.execute("CREATE TABLE PortInfo (SwitchID integer,ISCID integer,PortID integer,MLAGID integer, \
    VlanName Text,VlanTag integer,Tagged integer, \
    PRIMARY KEY(SwitchID,VlanTag),FOREIGN KEY (MLAGID) REFERENCES MLAGPeer(MLAGID), FOREIGN KEY(SwitchID) REFERENCES SwitchID(SwitchID))")

    c.execute("CREATE INDEX SearchPort on PortInfo (SwitchID,ISCID,PortID,MLAGID)")

def AddMLAGPeerInstance(SwitchID,ISCID,ISCPort,MLAGPeerName,VRName,LocalIPAddress,ISCVlanName,ISCIP,ISCVlanTag,ChkPtStatus,AuthMethod,NumMLAGPorts):
    """
    Adds Entry into the MLAGPeer table
    TBD : Add validations to each argument passed
    # AddMLAGPeerInstance(7,'sw2','VR-Default','51.2.2.1','two','51.2.2.2',2,'Up','None',1)
    :return:
    """

    global c

    #Validations - To be added

    #Check if the entry exists
    result=c.execute("SELECT * from MLAGPeer where ISCID= "+str(ISCID)+" and SwitchID= "+str(SwitchID)+" ;")
    Complete = result.fetchall()
    if len(Complete) != 0:
        logging.info("The table is empty")
    else:
        logging.info("The value is %s",Complete)

    result=c.execute("INSERT INTO MLAGPeer VALUES ("+str(SwitchID)+ ","+ str(ISCID)+","+str(ISCPort)+",'"+MLAGPeerName+"','"+ \
                    VRName+"','"+LocalIPAddress+"','" +ISCVlanName +"','"+ ISCIP +"',"+ \
                     str(ISCVlanTag) +",'"+ChkPtStatus+"','"+AuthMethod+"',"+str(NumMLAGPorts)+");")
    Complete = result.fetchall()
    logging.debug("The SQL INSERT command result is %s",Complete)


#  (SwitchID integer,ISCID integer,PortID integer,MLAGID integer,  VlanName Text,VlanTag integer,Tagged integer, PRIMARY KEY(SwitchID,VlanTag)
def AddPortInfo(SwitchID,ISCID,PortID,MLAGID,VlanName,VlanTag,Tagged):
    """
    Adds Entry into the portInfo table
    TBD : Add validations into each argument
    :param PortID:
    :param MLAGID:
    :param AdminState:
    :param LinkState:
    :param VlanName:
    :param VlanTag:
    :param Tagged:
    :return:
    """
    global c

    #Validations - To be added

    #Check if the entry exists
    result=c.execute("SELECT * from PortInfo where PortId="+str(PortID)+" and MLAGID = " + str(MLAGID) + " and VlanTag = " + str(VlanTag) + " and SwitchID= " + str(SwitchID)+ " ;")
    Complete = result.fetchall()
    if len(Complete) != 0:
        logging.info("The table is empty")
    else:
        logging.debug("The value is %s",Complete)

    result=c.execute("INSERT INTO PortInfo VALUES ("+str(SwitchID) + ","+str(ISCID)+"," + str(PortID)+","+str(MLAGID) + " ,'"  \
                    +VlanName+ "'," + str(VlanTag) + "," + str(Tagged) +");")
    Complete = result.fetchall()
    logging.debug("The SQL INSERT command result is %s",Complete)

def DeleteTables():
    """
    Delets both the MLAGPeer and the PortInfo tables
    :return:
    """
    # Delete Table
    global conn
    global c

    c.execute("drop index SearchPort")

    #Check if table MLAGPeer exists
    result = c.execute("PRAGMA table_info(MLAGPeer)")
    Complete = result.fetchall()
    if len(Complete) != 0:
        c.execute("drop table MLAGPeer")
        logging.info("THe table MLAGPeer exists and is deleted as part of cleanup")

    result = c.execute("PRAGMA table_info(PortInfo)")
    Complete = result.fetchall()
    if len(Complete) != 0:
        c.execute("drop table PortInfo")
        logging.info("THe table PortInfo exists and is deleted as part of cleanup")



def CloseDatabase():
    """
    Closes the connection to the database
    :return:
    """
    global conn
    global c
    c.close()
    conn.close()

def DebugShowMLAGTable():
    """
    Debug function to view the MLAG table
    :return:
    """
    global c

    result=c.execute("SELECT * from MLAGPeer")
    ResultsList=result.fetchall()

    for row in ResultsList:
        logging.info(row)


def DebugShowPortTable():
    """
    Debug function to view the Port table
    :return:
    """
    global c

    result=c.execute("SELECT * from PortInfo")
    ResultsList=result.fetchall()

    for row in ResultsList:
        logging.info(row)