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
    c = MLAGSQL.c

    result=c.execute("SELECT  SwitchID,ISCID,PeerIPAddress,ISCIP,ChkPtStatus,AuthMethod from MLAGPeer")
    ResultsList=result.fetchall()

    for row in ResultsList:
        logging.info(row)

# Get a list of Switch Pair IDs
    result=c.execute("SELECT DISTINCT S1.SwitchID,S2.SwitchID from MLAGPeer S1,MLAGPeer S2 where S1.PeerIPAddress==S2.ISCIP and S2.PeerIPAddress== S1.ISCIP and S1.SwitchID < S2.SwitchID")
    ResultsList=result.fetchall()

# Checking for Checkpoint Status is all switches
    ChkPtFlag = 0
    for SwitchPair in ResultsList:
        logging.info(SwitchPair)
        logging.info("The first peer switch is %s and the second peer switch is %s",SwitchPair[0],SwitchPair[1])

        CPResult=c.execute("SELECT S1.ChkPtStatus from MLAGPeer S1,MLAGPeer S2 where (S1.SwitchID="+str(SwitchPair[0])+" AND S2.SwitchID="+str(SwitchPair[1])+" AND \
         (S1.PeerIPAddress==S2.ISCIP and S2.PeerIPAddress== S1.ISCIP)) OR (S2.SwitchID="+str(SwitchPair[0])+" AND S1.SwitchID="+str(SwitchPair[1])+" AND \
         (S2.PeerIPAddress==S1.ISCIP and S1.PeerIPAddress== S2.ISCIP));")
        CPStatus=CPResult.fetchall()
        logging.info(CPStatus)
        for ChkPtStatus in CPStatus:

            logging.info("The checkpoint status is %s",ChkPtStatus[0])
            if ChkPtStatus[0] != "Up":
                print("Check point status is not up for MLAG Peer "+str(SwitchPair[0]) +" and " + str(SwitchPair[1]))
                logging.error("Check point status is not up for MLAG Peer %s and %s",str(SwitchPair[0]),str(SwitchPair[1]))

                ChkPtFlag =1

    if ChkPtFlag == 0 :
        print ("All Checkpoints are up and working fine")

# Checking for AuthMethod is all switches
    for SwitchPair in ResultsList:
        logging.info(SwitchPair)
        logging.info("The first peer switch is %s and the second peer switch is %s",SwitchPair[0],SwitchPair[1])

        AMResult=c.execute("SELECT DISTINCT S1.AuthMethod from MLAGPeer S1,MLAGPeer S2 where (S1.SwitchID="+str(SwitchPair[0])+" AND S2.SwitchID="+str(SwitchPair[1])+" AND \
         (S1.PeerIPAddress==S2.ISCIP and S2.PeerIPAddress== S1.ISCIP)) OR (S2.SwitchID="+str(SwitchPair[0])+" AND S1.SwitchID="+str(SwitchPair[1])+" AND \
         (S2.PeerIPAddress==S1.ISCIP and S1.PeerIPAddress== S2.ISCIP));")
        AMStatus=AMResult.fetchall()

        Length=len(AMStatus)

        logging.info("The length is %d",Length)

        if Length == 1:
            print("The Auth method of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " are the same")
        else :
            print("The Auth method of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")
            logging.error("The Auth method of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")

    # For each pair check the NumMlagPorts Status
    for SwitchPair in ResultsList:
        logging.info(SwitchPair)
        logging.info("The first peer switch is %s and the second peer switch is %s",SwitchPair[0],SwitchPair[1])

        NMPResult=c.execute("SELECT DISTINCT S1.NumMLAGPorts from MLAGPeer S1,MLAGPeer S2 where (S1.SwitchID="+str(SwitchPair[0])+" AND S2.SwitchID="+str(SwitchPair[1])+" AND \
         (S1.PeerIPAddress==S2.ISCIP and S2.PeerIPAddress== S1.ISCIP)) OR (S2.SwitchID="+str(SwitchPair[0])+" AND S1.SwitchID="+str(SwitchPair[1])+" AND \
         (S2.PeerIPAddress==S1.ISCIP and S1.PeerIPAddress== S2.ISCIP));")
        NMPStatus=NMPResult.fetchall()

        Length=len(NMPStatus)

        logging.info("The length is %d",Length)

        if Length == 1:
            print("The number of MLAG ports of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " are the same")
        else :
            print("The number of MLAG ports of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")
            logging.error("The Number of MLAG ports of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")

