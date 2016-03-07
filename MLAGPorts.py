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
    lines = mlag_port.splitlines()
    for x in lines:
        mlag_info = re.search('^([0-9]+)\s*([0-9]+)\s', x)
        if mlag_info:
            if mlag_info.group(1):
                mlag_id.append(mlag_info.group(1))
            if mlag_info.group(2):
                port_id.append(mlag_info.group(2))


    ### Show ports details for every port to capture the associated Vlan information
    for index1,index2 in zip(port_id,mlag_id):
        port_information = Library.SendCmd(handle, "show ports %s information detail" % (index1))
        Port_Vlan_info = re.findall('Name:.(.+?),.*Tag =.(.+?),.*\n\s+(Port.*:.*[0-9]*|(?!Port))', port_information)
        if Port_Vlan_info:
            for index in Port_Vlan_info:
                        index = list(index)
                        if "Port" in index[2]:
                               index[2] = 1
                        else:
                               index[2] = 0
                        print "switch,isc,%s,%s,%s,%s,%s" % (index1, index2, index[0], index[1], index[2])
    ### AddPortInfo(SwitchID, ISC_id, Port_id, Mlag_id, VlanName, VlanTag, Tag|Untag)
                        AddPortInfo(SwitchID, ISC_id, index1, index2, index[0], index[1], index[2])

### Note : Need to work for a solution for the ISC ID fetching and Error Handle
                                        

