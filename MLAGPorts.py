import connect
import Library
import MLAGSQL
import logging
import re
import connect


#####################################################################################################
#
#   AddPortInfo Procedure - Populate the AddPortInfo Table
#   -> Fetch the Mlag Ports and populate the Vlan details of each port
#   -> Fetch the ISC Port details from MLAGPEER table and Populate the VLAN information of each port
######################################################################################################

def MlagPort(handle, SwitchID):

    ### Disable CLI Paging to capture the whole output from the CLI
    print ("[] Diag: Checking MLAG Port Configuration for Switch %s .." %(connect.SwitchID_switchInfo[int(SwitchID)][0]))
    Library.SendCmd(handle, "disable clipaging")

### Show Mlag ports to capture MLAG id, Port ID and MLAG Peer Info in  Lists(mlag_id, port_id, mlag_peer )
    # "Show Mlag Ports" command to fetch the Mlag information (mlag_id, port_id, mlag_peer) in table format
    mlag_port = Library.SendCmd(handle, "show mlag ports")
    # List initialization
    port_id = []
    mlag_id = []
    mlag_peer = []
    Failure = 0
    # Splitting the lines in order to perform REGEX over a table data
    lines = mlag_port.splitlines()
    # Iterating for each line of the table data
    for x in lines:
        # Regex for the mlag_id, port_id, mlag_peer in format (45   22  A  Up  Peer1)
        mlag_info = re.search(
            '^([0-9]+)\s+([0-9]+(:[0-9]+|(?!:)))\s+(A|R|D|NP)\s+(Up|Down|N\/A)\s+([A-Za-z][A-Za-z0-9-_]+)\s+', x)
        if mlag_info:
            if mlag_info.group(1):
                # Record for MLAG ID
                mlag_id.append(mlag_info.group(1))
            else:
                logging.error("Configuration Issue : The Mlag ID is not found")
                print ("\tFAIL: Configuration Issue : The Mlag ID is not found")
                Failure = Failure + 1
            if mlag_info.group(2):
                # Record for MLAG Ports
                port_id.append(mlag_info.group(2))
            else:
                logging.error("Configuration Issue : The Port ID is not found")
                print ("\tFAIL: Configuration Issue : The Port ID is not found")
                Failure = Failure + 1
            if mlag_info.group(6):
                # Record for MLAG Peer Information
                mlag_peer.append(mlag_info.group(6))
            else:
                logging.error("Configuration Issue : Mlag Peer is not found")
                print ("\tFAIL: Configuration Issue : Mlag Peer is not found")
                Failure = Failure + 1
    if not mlag_id:
        Failure = Failure + 1
        print ("\tFAIL: No MLAG Ports Found for this SwitchID %s" %(SwitchID))



### Show ports details for every MLAG port to capture the associated Vlan information
    for index1, index2, index3 in zip(port_id, mlag_id, mlag_peer):
        # "Show Ports Information detail" command to fetch the Vlan Infomation for each MLAG Port
        port_information = Library.SendCmd(handle, "show ports %s information detail" % (index1))
        # Fetch the ISCID data from the MLAGPEER table
        ISC_id = MLAGSQL.c.execute(
            "SELECT ISCID from MLAGPeer where SwitchID = '%s' and MLAGPeerName = '%s'" % (SwitchID, index3))
        ISCList = ISC_id.fetchall()
        # REGEX the Port information output for obtaining the Vlan_Name, Vlan_Tag, Tagged|Untagged
        Port_Vlan_info = re.findall('Name:.(.+?),.*Tag =.(.+?),.*\n\s+(Port.*:.*[0-9]*|(?!Port))', port_information)
        if Port_Vlan_info:
            # If Tag information (eg: Port specific tag) found then Tagging is 1 else Tagging is 0
            for index in Port_Vlan_info:
                index = list(index)
                if "Port" in index[2]:
                    index[2] = 1
                else:
                    index[2] = 0
### AddPortInfo(SwitchID, ISC_id, Port_id, Mlag_id, VlanName, VlanTag, Tag|Untag)
                MLAGSQL.AddPortInfo(SwitchID, ISCList[0][0], index1, index2, index[0], index[1], index[2])
        else:
            logging.error("Configuration Issue : No Vlan Information found for respective port %s" % (index1))
            print ("\tFAIL: Configuration Issue : No Vlan Information found for respective port %s  in MLAG ID %s" % (index1,index2))
            Failure = Failure + 1

   ### Union of the List MLAG Peer to obtain a List of distict MLAG Peers
    mlag_peer = set(mlag_peer).union(mlag_peer)

### ISC Vlan Information Population
    for peer in mlag_peer:
        # Obtain the Distict ISIC ID from the MLAGPeer Table
        ISC_ID = MLAGSQL.c.execute(
            "SELECT DISTINCT ISCID from MLAGPeer where SwitchID = '%s' and MLAGPeerName = '%s'" % (SwitchID, peer))
        ISCid = ISC_ID.fetchall()
        for id in ISCid:
            # Obtain the ISC Port for each ISCID and SwitchID pair
            ISC_Port = MLAGSQL.c.execute(
                "SELECT ISCPort from MLAGPeer where SwitchID = '%s' and MLAGPeerName = '%s' and ISCID = '%s'" % (
                SwitchID, peer, id[0]))
            ISCport = ISC_Port.fetchall()
            if ISCport[0][0]:
                # Show Port information detail to obtain the ISC Vlan information details
                ISC_Port_Vlan_output = Library.SendCmd(handle, "show ports %s information detail" % str(ISCport[0][0]))
                # REGEX the Port information output for obtaining the Vlan_Name, Vlan_Tag, Tagged|Untagged
                ISC_Port_Vlan_info = re.findall('Name:.(.+?),.*Tag =.(.+?),.*\n\s+(Port.*:.*[0-9]*|(?!Port))',
                                                ISC_Port_Vlan_output)
                if ISC_Port_Vlan_info:
                    for index in ISC_Port_Vlan_info:
                        # If Tag information (eg: Port specific tag) found then Tagging is 1 else Tagging is 0
                        index = list(index)
                        if "Port" in index[2]:
                            index[2] = 1
                        else:
                            index[2] = 0
    ### AddPortInfo(SwitchID, ISC_id, Port_id, 0, VlanName, VlanTag, Tag|Untag) with MLAG ID = 0
                        MLAGSQL.AddPortInfo(SwitchID, id[0], ISCport[0][0], 0, index[0], index[1], index[2])
                else:
                       logging.error("Configuration Issue : No Vlan Information found for respective ISC port %s" % (ISCport[0][0]))
                       print ("\tFAIL: Configuration Issue : No Vlan Information found for respective ISC port %s" % (ISCport[0][0]))
                       Failure = Failure + 1

            else:
                logging.error("Configuration Issue : No ISC Port Information found for respective Peer %s and ISCID %s" % (peer, id[0]))
                print ("\tFAIL: Configuration Issue : No ISC Port Information found for respective Peer %s and ISCID %s" % (peer, id[0]))
                Failure = Failure + 1
                continue


    if Failure == 0:
        #print ("\tPASS: Checking MLAG Port Configuration for SwitchID %s" %(SwitchID))
        print ("")
    #else:
        #print ("\tFAIL: Checking MLAG Port Configuration for SwitchID %s" %(SwitchID))