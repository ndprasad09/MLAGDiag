import MLAGSQL
import logging
import Library


def interVLANCheck():
    Error_Logs = []
    Pass_Logs = []

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
                        Error_Logs.append("MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[1]))
            diffMlag2 = [x for x in MLAGList2 if x not in set(MLAGList1)]
            if len(diffMlag2):
                for eachDiff in diffMlag2:
                    if eachDiff != 0:
                        logging.error("MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[0]))
                        Error_Logs.append("MLAG ID %d is not Present in SwitchID %d" % (eachDiff, eachSwitch[0]))

            commonList = sorted(set(MLAGList1).intersection(MLAGList2))
            if len(commonList) != 0:
                for eachListItem in commonList:
                    if eachListItem == 0:
                        continue
                    else:
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
                                logging.error("VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[1], eachListItem))
                                Error_Logs.append("VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[1], eachListItem))
                            else:
                                UnTag = UnTag + 1
                                logging.info("Port %s in VLAN %s is UnTagged in Switch ID %d for MLAG ID %s" % (
                                    PortList1[0], TagListName1[index], eachSwitch[0], eachListItem))

                        diffTagList2 = [x for x in TagList2 if x not in set(TagList1)]
                        for eachElement in diffTagList2:
                            index = TagList2.index(eachElement)
                            TagFlag = TagFlag2[index]
                            if TagFlag == 1:
                                logging.error("VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[0], eachListItem))
                                Error_Logs.append("VLAN with Tag %d is not Present in Switch ID %d for MLAG ID %s" % (
                                    eachElement, eachSwitch[0], eachListItem))
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
                            logging.error("UnTag VLAN Mismatch between Peers %s and %s" % (PeerName1[0], PeerName2[0]))
                            Error_Logs.append(
                                "UnTag VLAN Mismatch between Peers %s and %s" % (PeerName1[0], PeerName2[0]))

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
                                            "Port %s in VLAN %s is added as Tagged in Switch ID %d and Port %s VLAN %s is added as Untagged in Switch ID %d for MLAG ID %s" % (
                                                PortList1[0], litem1[0], eachSwitch[0], PortList2[0], litem2[0],
                                                eachSwitch[1], eachListItem))
                                        Error_Logs.append(
                                            "Port %s in VLAN %s is added as Tagged in Switch ID %d and  Port %s in VLAN %s is added as Untagged in Switch ID %d for MLAG ID %s" % (
                                                PortList1[0], litem1[0], eachSwitch[0], PortList2[0], litem2[0],
                                                eachSwitch[1], eachListItem))
                                    else:
                                        logging.error(
                                            "Port %s in VLAN %s is added as Tagged in Switch ID %d and Port %s in VLAN %s is added as Untagged in Switch ID %d for MLAG ID %s" % (
                                                PortList2[0],litem2[0], eachSwitch[1], PortList1[0],litem1[0], eachSwitch[0], eachListItem))
                                        Error_Logs.append(
                                            "Port in VLAN %s is added as Tagged in Switch ID %d and Port %s in VLAN %s is added as Untagged in Switch ID %d for MLAG ID %s" % (
                                                PortList2[0],litem2[0], eachSwitch[1], PortList1[0],litem1[0], eachSwitch[0], eachListItem))


                                        # Library.print_error(Error_Logs)

    else:
        logging.info("No Items to be Compared between Switch")
        return











