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
    print ("[] Diag: Validating MLAG Peer Status")
    print ("\tTEST: To validate MLAG Check-Point, Auth & MLAG ports Status")
    for row in ResultsList:
        logging.info(row)

# Get a list of Switch Pair IDs
    result=c.execute("SELECT DISTINCT S1.SwitchID,S2.SwitchID from MLAGPeer S1,MLAGPeer S2 where S1.PeerIPAddress==S2.ISCIP and S2.PeerIPAddress== S1.ISCIP and S1.SwitchID < S2.SwitchID")
    ResultsList=result.fetchall()
    #replaceISCID(ResultsList)


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
                print("\tFAIL: Check point status is not up for MLAG Peer "+str(SwitchPair[0]) +" and " + str(SwitchPair[1]))
                logging.error("Check point status is not up for MLAG Peer %s and %s",str(SwitchPair[0]),str(SwitchPair[1]))

                ChkPtFlag =1

    if ChkPtFlag == 0 :
        print ("\tPASS: Check-Point Status is UP between peers")

        #Get DIstint ISCIds
        # FOR each ISC ID get the lis tof auth methods
        # pRint it
        # Compare

        ISCResult=c.execute("SELECT DISTINCT ISCID from MLAGPeer")

        ISCList = ISCResult.fetchall()

        for ISCID in ISCList:
            AuthResult=c.execute("SELECT DISTINCT AuthMethod from MLAGPeer where ISCID=" + str(ISCID[0])+";")

            AuthList = AuthResult.fetchall()

            for AuthMethod in AuthList:
                logging.info(AuthMethod)
            Length = len(AuthList)

            logging.info("Length of AuthList is %d",Length)
            if Length == 1:
                print("\tPASS: The Auth method of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " are same")
            else :
                print("\tFAIL: The Auth method of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")
                logging.error("The Auth method of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")

        for ISCID in ISCList:
            PortResult=c.execute("SELECT DISTINCT NumMLAGPorts from MLAGPeer where ISCID=" + str(ISCID[0])+";")

            PortList = PortResult.fetchall()

            for NumPorts in PortList:
                logging.info(NumPorts)
            Length = len(PortList)

            logging.info("Length of PortList is %d",Length)
            if Length == 1:
                print("\tPASS: The number of MLAG ports of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " are same")
            else :
                print("\tFAIL: The number of MLAG ports of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")
                logging.error("The Number of MLAG ports of Peer " + str(SwitchPair[0])+ " and Peer "+ str(SwitchPair[1])+ " do not match")

    print ("")

def replaceISCID():

    c =MLAGSQL.c

    result=c.execute("SELECT DISTINCT S1.ISCID,S2.ISCID from MLAGPeer S1,MLAGPeer S2 where S1.PeerIPAddress==S2.ISCIP and S2.PeerIPAddress== S1.ISCIP and S1.SwitchID < S2.SwitchID")
    retList = result.fetchall()
    for eachItem in retList:
        c.execute("UPDATE MLAGPeer SET ISCID="+str(eachItem[0])+" where ISCID="+str(eachItem[1])+"")


    MLAGSQL.DebugShowMLAGTable()




