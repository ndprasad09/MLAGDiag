import MLAGSQL
import logging
import Library
import connect

"""
This Procedure compares MLAG and VLAN Information
Between MLAG Peers and displays the Error logs
if anything found
:return: None
"""
def interVLANCheck():

    Error_Logs = []
    Pass_Logs = []
    print ("[] Diag: VLAN and MLAG ID Comparisons Between MLAG Peers")
    retList = MLAGSQL.returnQuery("SELECT DISTINCT ISCID from PortInfo")
    ISCList = []
    MainList = []

    for eachVal in retList:
        ISCList.append(eachVal[0])

    for eachISC in ISCList:
        strISC = str(eachISC)
        retList = MLAGSQL.returnQuery("SELECT DISTINCT SwitchID from PortInfo WHERE ISCID=" + strISC + "")
        tempList = []
        if len(retList) == 2:
            for eachItem in retList:
                # tempList = []
                tempList.append(eachItem[0])
            tempList.append(eachISC)
            MainList.append(tempList)
        else:
            switchID = retList[0][0]
            print ("\tFAIL: No Valid MLAG Peer detected for Switch with IP %s" %(connect.SwitchID_switchInfo[int(switchID)][0]))
            continue

    if len(MainList) != 0:

        for eachSwitch in MainList:
            #print ("[] Diag: VLAN Comparisons between Peers %d and %d:" % (eachSwitch[0],eachSwitch[1]))

            MLAGList1 = []
            MLAGList2 = []
            Mlagid_error = 0
            ISC = str(eachSwitch[2])
            switchID1 = str(eachSwitch[0])
            switchID2 = str(eachSwitch[1])
            print ("\tTEST: MLAG ID Comparison between Peers %s and %s" %(connect.SwitchID_switchInfo[int(switchID1)][0],connect.SwitchID_switchInfo[int(switchID2)][0]))
            tempMLAGList1 = MLAGSQL.returnQuery(
                "SELECT DISTINCT MLAGID from PortInfo WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + "")

            tempMLAGList2 = MLAGSQL.returnQuery(
                "SELECT DISTINCT MLAGID from PortInfo WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + "")
            for eachMLAG in tempMLAGList1:
                MLAGList1.append(eachMLAG[0])
            for eachMLAG in tempMLAGList2:
                MLAGList2.append(eachMLAG[0])

            diffMlag1 = [x for x in MLAGList1 if x not in set(MLAGList2)]
            if len(diffMlag1) != 0:
                for eachDiff in diffMlag1:


                    if eachDiff != 0:
                        logging.error("\tFAIL: MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[1]))
                        print("\tFAIL: MLAG ID %d may not be Present in Switch %s or MLAG Port is not associated with any VLAN" % (eachDiff, connect.SwitchID_switchInfo[int(eachSwitch[1])][0]))
                        Mlagid_error = Mlagid_error + 1
            diffMlag2 = [x for x in MLAGList2 if x not in set(MLAGList1)]
            if len(diffMlag2):
                for eachDiff in diffMlag2:


                    if eachDiff != 0:
                        logging.error("\tFAIL: MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[0]))
                        print ("\tFAIL: MLAG ID %d may not be Present in Switch %s or MLAG Port is not associated with any VLAN" % (eachDiff, connect.SwitchID_switchInfo[int(eachSwitch[0])][0]))
                        Mlagid_error = Mlagid_error + 1

            if Mlagid_error == 0:
                print ("\tPASS: MLAG ID Comparison passed between Peers %s and %s" %(connect.SwitchID_switchInfo[int(switchID1)][0],connect.SwitchID_switchInfo[int(switchID2)][0]))
            commonList = sorted(set(MLAGList1).intersection(MLAGList2))
            #commonList.remove(0) #Removing MLAGID of ISC Vlan. 0 is MLAG ID of ISC VLAN
            if len(commonList) != 0:

                for eachListItem in commonList:
                    error_flag = 0
                    if eachListItem == 0:

                        eachListItem = str(eachListItem)
                        print ("\tTEST: Checking ISC VLAN Configuration between Peers %s and %s" %(connect.SwitchID_switchInfo[int(switchID1)][0],connect.SwitchID_switchInfo[int(switchID2)][0]))

                        #Querying Information from SwitchID1
                        ISCVlanName = MLAGSQL.returnQuery("SELECT ISCVlanName from MLAGPeer WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + "")
                        tempISCList1 = MLAGSQL.returnQuery(
                           "SELECT VlanTag,Tagged from PortInfo WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + "  AND VlanName='%s'" % (ISCVlanName[0][0]))

                        if len(tempISCList1) != 0:
                            ISCVlanList1 = tempISCList1[0]
                        else:
                            logging.error("ISC Vlan Information not found for Switch IP %s" %(connect.SwitchID_switchInfo[int(switchID1)][0]))

                        #Querting Information from Switch ID2
                        ISCVlanName = MLAGSQL.returnQuery("SELECT ISCVlanName from MLAGPeer WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + "")
                        tempISCList2 = MLAGSQL.returnQuery(
                           "SELECT VlanTag,Tagged from PortInfo WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + "  AND VlanName='%s'" % (ISCVlanName[0][0]))

                        if len(tempISCList2) != 0:
                            ISCVlanList2 = tempISCList2[0]
                        else:
                            logging.error("ISC Vlan Information not found for Switch IP %s" %(connect.SwitchID_switchInfo[int(switchID2)][0]))


                        #ISC VLAN Comparison


                        TagFlag1 = ISCVlanList1[1]
                        TagFlag2 = ISCVlanList2[1]
                        if TagFlag1 == TagFlag2:
                            if TagFlag1 == 1: #Condition for Tagged
                                if TagFlag1 != TagFlag2:
                                    print ("\tFAIL: ISC VLAN Tag does not match between peers %s and %s" % (connect.SwitchID_switchInfo[int(switchID1)][0], connect.SwitchID_switchInfo[int(switchID2)][0]))
                                else:
                                    print ("\tPASS: ISC VLAN Comparison passed between peers %s and %s" % (connect.SwitchID_switchInfo[int(switchID1)][0], connect.SwitchID_switchInfo[int(switchID2)][0]))
                            else:
                                logging.info ("ISC Ports are added as Untagged between switch peers %s and %s"% (connect.SwitchID_switchInfo[int(switchID1)][0], connect.SwitchID_switchInfo[int(switchID2)][0]))
                                print ("\tPASS: ISC VLAN Comparison passed between peers %s and %s" % (connect.SwitchID_switchInfo[int(switchID1)][0], connect.SwitchID_switchInfo[int(switchID2)][0]))


                        else:

                            if TagFlag1 == 1:
                                print ("\tFAIL: ISC Port is added as Tagged in switch IP %s and Untagged in switch IP %s for ISC VLAN" % (connect.SwitchID_switchInfo[int(switchID1)][0], connect.SwitchID_switchInfo[int(switchID2)][0]))
                            else:
                                print ("\tFAIL: ISC Port is added as Tagged in switch IP %s and Untagged in switch IP %s for ISC VLAN" % (connect.SwitchID_switchInfo[int(switchID2)][0], connect.SwitchID_switchInfo[int(switchID1)][0]))





                        #print tempISCList2
                    else:
                        print ("\n")
                        print ("\tTEST: Checking VLAN Configurations Between Peers %s and %s for MLAG ID %d" %(connect.SwitchID_switchInfo[int(switchID1)][0],connect.SwitchID_switchInfo[int(switchID2)][0],eachListItem))
                        eachListItem = str(eachListItem)
                        tempVLANList1 = MLAGSQL.returnQuery(
                            "SELECT VlanName,VlanTag,Tagged from PortInfo WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + " AND MLAGID=" + eachListItem + "")
                        tempPortList1 = MLAGSQL.returnQuery(
                            "SELECT DISTINCT PortID from PortInfo WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + " AND MLAGID=" + eachListItem + "")
                        PortList1 = tempPortList1[0]
                        tempVLANList2 = MLAGSQL.returnQuery(
                            "SELECT VlanName,VlanTag,Tagged from PortInfo WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + " AND MLAGID=" + eachListItem + "")
                        tempPortList2 = MLAGSQL.returnQuery(
                            "SELECT DISTINCT PortID from PortInfo WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + " AND MLAGID=" + eachListItem + "")
                        PortList2 = tempPortList2[0]
                        VLANList1 = []
                        VLANList2 = []

                        for eachItem in range(0, len(tempVLANList1)):
                            VLANList1.append(tempVLANList1[eachItem])
                        for eachItem in range(0, len(tempVLANList2)):
                            VLANList2.append(tempVLANList2[eachItem])


                        # ---- List Initialization for each VLAN List in Switch Pair
                        TagListName1 = []
                        TagList1 = []
                        TagList2 = []
                        TagListName2 = []
                        TagFlag1 = []
                        TagFlag2 = []
                        # ---------------------------------------------------

                        for eachItem in VLANList1:
                            TagListName1.append(eachItem[0])
                            TagList1.append(eachItem[1])
                            TagFlag1.append(eachItem[2])

                        for eachItem in VLANList2:
                            TagListName2.append(eachItem[0])
                            TagList2.append(eachItem[1])
                            TagFlag2.append(eachItem[2])
                        # Gives a Difference between VLAN Tag Lists between Switch Pairs
                        # ----------------------------------------------------------------
                        diffTagList1 = [x for x in TagList1 if x not in set(TagList2)]
                        UnTag = 0
                        for eachElement in diffTagList1:
                            index = TagList1.index(eachElement)
                            TagFlag = TagFlag1[index]
                            if TagFlag == 1:
                                logging.error("\tFAIL: VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[1], eachListItem))
                                print("\tFAIL: VLAN with Tag %d is not Present in Switch with IP %s for MLAG ID %s" % (
                                    eachElement, connect.SwitchID_switchInfo[int(eachSwitch[1])][0], eachListItem))
                                error_flag = error_flag + 1
                            else:
                                UnTag = UnTag + 1
                                logging.info("\tPort %s in VLAN %s is UnTagged in Switch ID %d for MLAG ID %s" % (
                                    PortList1[0], TagListName1[index], eachSwitch[0], eachListItem))

                        diffTagList2 = [x for x in TagList2 if x not in set(TagList1)]
                        for eachElement in diffTagList2:
                            index = TagList2.index(eachElement)
                            TagFlag = TagFlag2[index]
                            if TagFlag == 1:
                                logging.error("\tFAIL: VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[0], eachListItem))
                                print("\tFAIL: VLAN with Tag %d is not Present in Switch with IP %s for MLAG ID %s" % (
                                    eachElement, connect.SwitchID_switchInfo[int(eachSwitch[0])][0], eachListItem))
                                error_flag  = error_flag + 1
                            else:
                                UnTag = UnTag + 1
                                logging.info("Port %s in VLAN %s is UnTagged in Switch ID %d for MLAG ID %s" % (
                                    PortList2[0], TagListName2[index], eachSwitch[1], eachListItem))
                        # ------------------------------------------------------------------------------
                        # ----- UnTag should be 2; for a given MLAG ID across Switch Pair
                        if UnTag == 1:
                            PeerName1 = MLAGSQL.returnQuery(
                                "SELECT MLAGPeerName from MLAGPeer WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + "")
                            PeerName2 = MLAGSQL.returnQuery(
                                "SELECT MLAGPeerName from MLAGPeer WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + "")
                            logging.error("\tFAIL: UnTag VLAN Mismatch between Peers %s and %s" % (PeerName1[0], PeerName2[0]))
                            print ("\tFAIL: UnTag VLAN Mismatch between Peers %s and %s for MLAG IP %s" % (PeerName1[0], PeerName2[0], eachListItem))
                            error_flag = error_flag + 1

                        # Matching VLAN Tags Between Between Two Switches

                        commonTagList = sorted(set(TagList1).intersection(TagList2))
                        if len(commonTagList) != 0:
                            compList1 = []
                            compList2 = []
                            for eachTag in commonTagList:
                                for eachTagInfo in VLANList1:
                                    if eachTag == eachTagInfo[1]:
                                        compList1.append(eachTagInfo)

                            for eachTag in commonTagList:
                                for eachTagInfo in VLANList2:
                                    if eachTag == eachTagInfo[1]:
                                        compList2.append(eachTagInfo)

                            for eachNum in range(0, len(compList1)):
                                litem1 = compList1[eachNum]
                                litem2 = compList2[eachNum]
                                if litem1[2] == litem2[2]:
                                    continue

                                else:
                                    if litem1[2] == 1:
                                        logging.error(
                                            "\tFAIL: Port %s in VLAN %s is added as Tagged in Switch with IP %s and Port %s VLAN %s is added as Untagged in Switch with IP %s for MLAG ID %s" % (
                                                PortList1[0], litem1[0], connect.SwitchID_switchInfo[eachSwitch[0]][0], PortList2[0], litem2[0],
                                                connect.SwitchID_switchInfo[eachSwitch[1]][0], eachListItem))
                                        print(
                                            "\tFAIL: Port %s in VLAN %s is added as Tagged in Switch ID %d and  Port %s in VLAN %s is added as Untagged in Switch ID %d for MLAG ID %s" % (
                                                PortList1[0], litem1[0], connect.SwitchID_switchInfo[int(eachSwitch[0])][0], PortList2[0], litem2[0],
                                                connect.SwitchID_switchInfo[int(eachSwitch[1])][0], eachListItem))
                                        error_flag = error_flag +1
                                    else:
                                        logging.error(
                                            "\tFAIL: Port %s in VLAN %s is added as Tagged in Switch ID %d and Port %s in VLAN %s is added as Untagged in Switch ID %d for MLAG ID %s" % (
                                                PortList2[0],litem2[0], eachSwitch[1], PortList1[0],litem1[0], eachSwitch[0], eachListItem))
                                        print(
                                            "\tFAIL: Port in VLAN %s is added as Tagged in Switch with IP %s and Port %s in VLAN %s is added as Untagged in Switch with IP %s for MLAG ID %s" % (
                                                PortList2[0],litem2[0], connect.SwitchID_switchInfo[int(eachSwitch[1])][0], PortList1[0],litem1[0], connect.SwitchID_switchInfo[int(eachSwitch[0])][0], eachListItem))
                                        error_flag = error_flag + 1

                            if error_flag == 0:
                                print ("\tPASS: VLAN Configuration Test Passed between Peers %s and %s for MLAG ID %s" %(connect.SwitchID_switchInfo[int(switchID1)][0],connect.SwitchID_switchInfo[int(switchID2)][0],eachListItem))


            else:
                print ("\tFAIL: No Common MLAG ID detected between Peer %s and %s" %(connect.SwitchID_switchInfo[switchID1][0],connect.SwitchID_switchInfo[switchID2][0]))
            #print ("VLAN Comparison Finished Between Peers %s and %s" %(switchID1,switchID2))

                                        # Library.print_error(Error_Logs)

    else:
        #logging.info("No Items to be Compared between Switch")
        print ("\tFAIL: No VLAN Comparisons between switch peers")
        return











