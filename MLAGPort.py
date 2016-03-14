import connect
import Library
import MLAGSQL
import logging
import re

#####################################################################################################
#
#   AddPortInfo Procedure - First Draft
#
######################################################################################################

def MlagPort(handle, SwitchID):
    
    ### Disable CLI Paging to capture the whole output from the CLI
    Library.SendCmd(handle, "disable clipaging")

    ### Show Mlag ports to capture MLAG id and Port ID in a Lists(mlag_id, port_id)
    mlag_port = Library.SendCmd(handle, "show mlag ports")
    port_id = []
    mlag_id = []
    mlag_peer = []
    lines = mlag_port.splitlines()
    for x in lines:
        mlag_info = re.search('^([0-9]+)\s+([0-9]+(:[0-9]+|(?!:)))\s+(A|R|D|NP)\s+(Up|Down|N\/A)\s+([A-Za-z][A-Za-z0-9]+)\s+', x)
        if mlag_info:
            if mlag_info.group(1):
                mlag_id.append(mlag_info.group(1))
            if mlag_info.group(2):
                port_id.append(mlag_info.group(2))
            if mlag_info.group(6):
                mlag_peer.append(mlag_info.group(6))
                

    ### Show ports details for every port to capture the associated Vlan information
    for index1,index2,index3 in zip(port_id,mlag_id,mlag_peer):
        port_information = Library.SendCmd(handle, "show ports %s information detail" % (index1))
        ISC_id = MLAGSQL.c.execute("SELECT ISCID from MLAGPeer where SwitchID = '%s' and MLAGPeerName = '%s'" % (SwitchID, index3))
        Port_Vlan_info = re.findall('Name:.(.+?),.*Tag =.(.+?),.*\n\s+(Port.*:.*[0-9]*|(?!Port))', port_information)
        if Port_Vlan_info:
            for index in Port_Vlan_info:
                        index = list(index)
                        if "Port" in index[2]:
                               index[2] = 1
                        else:
                               index[2] = 0
                        print "%s,%s,%s,%s,%s,%s,%s" % (SwitchID, ISC_id, index1, index2, index[0], index[1], index[2])
    ### AddPortInfo(SwitchID, ISC_id, Port_id, Mlag_id, VlanName, VlanTag, Tag|Untag)
                        MLAGSQL.AddPortInfo(SwitchID, ISC_id, index1, index2, index[0], index[1], index[2])


    for peer in mlag_peer:
        ISC_Port = MLAGSQL.c.execute("SELECT ISCPort in MLAGPeer where SwitchID = '%s' and MLAGPeerName = '%s'" % (SwitchID, peer))
        ISC_id = MLAGSQL.c.execute("SELECT ISCID from MLAGPeer where SwitchID = '%s' and MLAGPeerName = '%s'" % (SwitchID, peer))
        ISC_Port_Vlan_output = Library.SendACmd(handle, "show ports %s information detail" % (ISC_Port))
        ISC_Port_Vlan_info = re.findall('Name:.(.+?),.*Tag =.(.+?),.*\n\s+(Port.*:.*[0-9]*|(?!Port))', ISC_Port_Vlan_output)
        if ISC_Port_Vlan_info:
            for index in ISC_Port_Vlan_info:
                        index = list(index)
                        if "Port" in index[2]:
                               index[2] = 1
                        else:
                               index[2] = 0
                        print "%s,%s,0,%s,%s,%s" % (SwitchID, ISC_id, index[0], index[1], index[2])
                        MLAGSQL.AddPortInfo(SwitchID, ISC_id, ISC_Port, 0, index[0], index[1], index[2])
        
