import MLAGSQL
import logging

########################################################
# Global Variables
#########################################################
global conn
global c

def CheckMLAGStatus():
    """
    Compares the MLAG configuration in both switches and checks for any global config mismatch
    :param ISCID1:
    :param ISCID2:
    :return:
    """
    #logging.INFO("The ISCID 1 is %s and  ISCID2 is %s",ISCID1,ISCID2)

    ### TBD
    # Algorithm for Checking the Status
    # Get the ISC ID List from MLAGPeerTable
    # Find the ISC IDs of the peer switches
    # For each pair check the Checkpoint status
    # For each pair check the Auth Method Status
    # For each pair check the NumMlagPorts Status


    c = MLAGSQL.c

    result=c.execute("SELECT  SwitchID,ISCID,PeerIPAddress,ISCIP,ChkPtStatus,AuthMethod from MLAGPeer")
    ResultsList=result.fetchall()

    for row in ResultsList:
        logging.info(row)

    # Get the Switch Pairs

    # Get the ISC ID List
    result=c.execute("SELECT  DISTINCT ISCID from MLAGPeer")
    ResultsList=result.fetchall()

    for row in ResultsList:
        logging.info(row[0])
        result1=c.execute("SELECT SwitchID,PeerIPAddress,ISCIP from MLAGPeer where ISCID="+str(row[0]))
        ResultsList1=result1.fetchall()
        len2 = str(len(ResultsList1))
        print ("The length is ",len(ResultsList1))
       # logging.INFO("The length of the Result list is %d",len(ResultsList1))
        for row1 in ResultsList1:
            logging.info(row1)


