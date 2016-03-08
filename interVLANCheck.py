import MLAGSQL
import logging

def interVLANCheck():
    logging.basicConfig(level=logging.INFO)
    MLAGSQL.ConnectDatabase()
    MLAGSQL.CreateTables()
    MLAGSQL.AddMLAGPeerInstance(1, 1, 11, 'sw2', 'VR-Default', '51.2.2.1', 'two', '51.2.2.2', 2, 'Up', 'None', 1)
    MLAGSQL.AddMLAGPeerInstance(2, 1, 12, 'sw3', 'VR-Default', '41.2.2.2', 'three', '41.2.2.1', 3, 'Up', 'None', 1)
    MLAGSQL.AddMLAGPeerInstance(2,2,22,'sw3','VR-Default','31.2.2.2','three','31.2.2.1',4,'Up','None',1)
    MLAGSQL.AddMLAGPeerInstance(3,2,31,'sw1','VR-Default','41.2.2.1','two','41.2.2.2',2,'Up','None',1)
    #MLAGSQL.AddPortInfo(1, 1, 52, 0, 'v3', 3, 1)
    MLAGSQL.AddPortInfo(1, 1, 52, 7, 'v3', 3, 1)
    MLAGSQL.AddPortInfo(1, 1, 52, 7, 'v102', 102, 1)
    #MLAGSQL.AddPortInfo(1, 1, 52, 8, 'v4', 4, 1)
    #MLAGSQL.AddPortInfo(1, 1, 52, 8, 'v1000', 4093, 0)
    #MLAGSQL.AddPortInfo(1, 1, 52, 9, 'v5', 100, 1)
    MLAGSQL.AddPortInfo(2, 1, 52, 7, 'v5', 3, 1)
    #MLAGSQL.AddPortInfo(2, 1, 52, 7, 'v6', 102, 1)
    #MLAGSQL.AddPortInfo(2, 1, 52, 8, 'v1000', 4092, 0)
    #MLAGSQL.AddPortInfo(2, 1, 52, 10, 'v101', 101, 1)
    #MLAGSQL.AddPortInfo(2, 2, 53, 9, 'v7', 7, 1)
    #MLAGSQL.AddPortInfo(3, 2, 53, 9, 'v7', 7, 1)
    #MLAGSQL.AddPortInfo(3, 2, 52, 9, 'v100', 4095, 0)
    #MLAGSQL.AddPortInfo(2, 2, 52, 9, 'v100', 4095, 1)
    # MLAGSQL.DebugShowPortTable()
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
                #tempList = []
                tempList.append(eachItem[0])
            tempList.append(eachISC)
            MainList.append(tempList)
        else:
            continue

    if len(MainList) != 0:
        
        for eachSwitch in MainList:
            MLAGList1 = []
            MLAGList2 = []
            ISC = str(eachSwitch[2])
            switchID1 = str(eachSwitch[0])
            switchID2 = str(eachSwitch[1])
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
                        logging.error("MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[1]))
            diffMlag2 = [x for x in MLAGList2 if x not in set(MLAGList1)]
            if len(diffMlag2):
                for eachDiff in diffMlag2:
                    if eachDiff != 0:
                        logging.error("MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[0]))

            commonList = sorted(set(MLAGList1).intersection(MLAGList2))
            if len(commonList) != 0:
                for eachListItem in commonList:
                    if eachListItem == 0:
                        continue
                    else:
                        eachListItem = str(eachListItem)
                        tempVLANList1 = MLAGSQL.returnQuery(
                            "SELECT VlanName,VlanTag,Tagged from PortInfo WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + " AND MLAGID=" + eachListItem + "")
                        tempVLANList2 = MLAGSQL.returnQuery(
                            "SELECT VlanName,VlanTag,Tagged from PortInfo WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + " AND MLAGID=" + eachListItem + "")
                        VLANList1 = []
                        VLANList2 = []

                        for eachItem in range(0, len(tempVLANList1)):
                            VLANList1.append(tempVLANList1[eachItem])
                        for eachItem in range(0, len(tempVLANList2)):
                            VLANList2.append(tempVLANList2[eachItem])


                        #---- List Initialization for each VLAN List in Switch Pair
                        TagListName1 = []
                        TagList1 = []
                        TagList2 = []
                        TagListName2 = []
                        TagFlag1 = []
                        TagFlag2 = []
                        #---------------------------------------------------

                        for eachItem in VLANList1:
                            TagListName1.append(eachItem[0])
                            TagList1.append(eachItem[1])
                            TagFlag1.append(eachItem[2])

                        for eachItem in VLANList2:
                            TagListName2.append(eachItem[0])
                            TagList2.append(eachItem[1])
                            TagFlag2.append(eachItem[2])
                        # Gives a Difference between VLAN Tag Lists between Switch Pairs
                        #----------------------------------------------------------------
                        diffTagList1 = [x for x in TagList1 if x not in set(TagList2)]
                        UnTag = 0
                        for eachElement in diffTagList1:
                            index = TagList1.index(eachElement)
                            TagFlag = TagFlag1[index]
                            if TagFlag == 1:
                                logging.error("VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[1], eachListItem))
                            else:
                                UnTag = UnTag + 1
                                logging.info("VLAN %s is UnTagged in Switch ID %d for MLAG ID %s" % (
                                    TagListName1[index], eachSwitch[0], eachListItem))

                        diffTagList2 = [x for x in TagList2 if x not in set(TagList1)]
                        for eachElement in diffTagList2:
                            index = TagList2.index(eachElement)
                            TagFlag = TagFlag2[index]
                            if TagFlag == 1:
                                logging.error("VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[0], eachListItem))
                            else:
                                UnTag = UnTag + 1
                                logging.info("VLAN %s is UnTagged in Switch ID %d for MLAG ID %s" % (
                                    TagListName2[index], eachSwitch[1], eachListItem))
                        #------------------------------------------------------------------------------
                        #----- UnTag should be 2; for a given MLAG ID across Switch Pair
                        if UnTag == 1:
                            PeerName1 = MLAGSQL.returnQuery(
                                "SELECT MLAGPeerName from MLAGPeer WHERE SwitchID=" + switchID1 + " AND ISCID=" + ISC + "")
                            PeerName2 = MLAGSQL.returnQuery(
                                "SELECT MLAGPeerName from MLAGPeer WHERE SwitchID=" + switchID2 + " AND ISCID=" + ISC + "")
                            logging.error("UnTag VLAN Mismatch between Peers %s and %s" % (PeerName1[0], PeerName2[0]))

                        #Matching VLAN Tags Between Between Two Switches

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

                            for eachNum in range(0,len(compList1)):
                                litem1 = compList1[eachNum]
                                litem2 = compList2[eachNum]
                                if litem1[2] == litem2[2]:
                                    continue

                                else:
                                    if litem1[2] == 1:
                                        logging.error("VLAN %s is added as Tagged in Switch ID %d and VLAN %s is added as Untagged in Switch ID %d" %(litem1[0],eachSwitch[0],litem2[0],eachSwitch[1]))
                                    else:
                                        logging.error("VLAN %s is added as Tagged in Switch ID %d and VLAN %s is added as Untagged in Switch ID %d" %(litem2[0],eachSwitch[1],litem1[0],eachSwitch[0]))



    else:
        logging.info("No Items to be Compared between Switch Pairs")
        return




if __name__ == "__main__":
    interVLANCheck()






