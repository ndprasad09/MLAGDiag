import MLAGSQL
import logging
import connect
import Library
import re
def get_mlag_peer(handler,SwitchID):
    """
    This procedure collects MLAG Peer Informations
    and inserts in to the table MLAGPeerInstance

    :param handler: connection handler to the switch
    :param SwitchID: Switch ID
    :return: none

    """
    #-- Initialize the local variables
    ISCVlan = ""
    VirtualRouter = ""
    CheckpointStatus = ""
    Authentication = ""
    PeerName = ""
    ISCPort = 0

    #-- Disable cli paging in swictch
    Library.SendCmd(handler,"disable clipaging")
    #-- Get the show mlag peer output
    output = Library.SendCmd(handler,"show mlag peer")

    #-- Parse the output for required fields to feed to MLAGPeer table
    #-- Peer Name
    PeerNameexist = re.search(r"MLAG\s+Peer\s+:\s+(\w+)\s+.*",output)
    if PeerNameexist:
        PeerName = PeerNameexist.groups(1)[0]
    #-- Virtual router
    VirtualRouterexist = re.search (r"Virtual\s+Router\s+:\s+(.*)\s+\r",output)
    if VirtualRouterexist:
          VirtualRouter = VirtualRouterexist.groups(1)[0]
    #-- Checkpointstatus
    CheckpointStatusexist = re.search (r"Checkpoint\s+Status\s+:\s+(Up|Down)\s+.*",output)
    if CheckpointStatusexist:
        CheckpointStatus=CheckpointStatusexist.groups(1)[0]
    #-- Authentication
    Authenticationexist = re.search(r"Authentication\s+:\s+(\w+)\s+.*",output)
    if Authenticationexist:
        Authentication = Authenticationexist.groups(1)[0]
    #-- ISC vlan
    ISCVlanpresent = re.search (r"VLAN\s+:\s+(\w+)\s+.*",output)
    if ISCVlanpresent:
        ISCVlan = ISCVlanpresent.groups(1)[0]
        IPAddress=re.search (r"Local\s+IP\s+Address\s+:\s+(\d+\.\d+\.\d+\.\d+)\s+Peer\s+IP\s+Address\s+:\s+(\d+\.\d+\.\d+\.\d+)",output)
        LocalIPAddress = IPAddress.groups(1)[0]
        PeerIPAddress = IPAddress.groups(1)[1]
    else:
        print "No ISCVlan present"

    #-- MLAG Ports
    match=re.search (r"MLAG.*ports\s+:\s+(\d+)\s+.*",output)
    if match:
        MLAGPorts = int(match.groups(1)[0])
    else:
        print "No Match for MLAG ports"

    #-- Get show isc vlan output from switch
    output2 = Library.SendCmd(handler,"show vlan "+ISCVlan)
    #-- ISC vlan specific information
    #-- Tag status
    TagInfo = re.search (r"Tagging:(.*)",output2)
    if TagInfo:
        Vlantag = TagInfo.groups(1)[0]
        Tagged = re.search (r"802\.1Q.*Tag\s+(\d+)",output2)

        if Tagged:
            ISCVlanID = Tagged.groups(1)[0]
            Ports = re.search(r"Ports.*Number.*active.*ports.*\n.*Tag:\s+(\w+).*\r",output2)
            if Ports:
                print Ports.groups(1)
                ISCPort = Ports.groups(1)[0]
            else:
                UntagPorts = re.search (r"Ports.*Number.*active.*ports.*\n.*Untag:\s+(\w+).*\r",output2)
                if UntagPorts:
                    ISCPort = UntagPorts.groups(1)[0]
                else:
                    print "No Ports found !!!"
        else:
            #-- Untagged ISC Vlan is given a tag of 12345
            ISCVlanID = 12345
            UntagPorts = re.search (r"Ports.*Number.*active.*ports.*\n.*Untag:\s+(\w+).*\r",output2)
            if UntagPorts:
                ISCPort = UntagPorts.groups(1)[0]
            else:
                print "No Ports found !!!"
    else:
        print "No Tag Info Present"

    #-- remove invalid characters from the port
    if ISCPort:
        ISCPort = ISCPort.strip('g')

    #-- Add to Database
    MLAGSQL.AddMLAGPeerInstance(1,1,ISCPort,PeerName,VirtualRouter,LocalIPAddress,ISCVlan,PeerIPAddress,ISCVlanID,CheckpointStatus,Authentication,1)