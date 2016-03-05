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
    PeerIPAddress = ""
    LocalIPAddress= ""
    ISCVlanID = 0

    #-- Disable cli paging in swictch
    Library.SendCmd(handler,"disable clipaging")
    #-- Get the show mlag peer output
    output = Library.SendCmd(handler,"show mlag peer")

    #-- Parse the output for required fields to feed to MLAGPeer table
    #-- Peer Name
    PeerNameexist = re.search(r"MLAG\s+Peer\s+:\s+(\w+)\s+.*",output)
    if PeerNameexist:
        PeerName = PeerNameexist.groups(1)[0]
    else :
        logging.error("No MLAG Peer Exists in Switch ID : "+str(SwitchID))
        logging.error("Returning with failure to update the MLAG Peer Instance")
        return

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

    #-- MLAG Ports
    match=re.search (r"MLAG.*ports\s+:\s+([1-9]+)\s+.*",output)
    if match:
        MLAGPorts = int(match.groups(1)[0])
    else:
        MLAGPorts = 0
        logging.error("No MLAG ports present")

    #-- ISC vlan
    ISCVlanpresent = re.search (r"VLAN\s+:\s+(\w+)\s+.*",output)
    if ISCVlanpresent:
        ISCVlan = ISCVlanpresent.groups(1)[0]
        LIPAddressexist=re.search (r"Local\s+IP\s+Address\s+:\s+(\d+\.\d+\.\d+\.\d+)\s+",output)
        if LIPAddressexist:
            LocalIPAddress = LIPAddressexist.groups(1)[0]
        else :
            logging.info("IPadrress not confgured for ISC vlan :"+ISCVlan)
        PIpAddressexist=re.search(r"Peer\s+IP\s+Address\s+:\s+(\d+\.\d+\.\d+\.\d+)",output)
        if PIpAddressexist:
            PeerIPAddress = PIpAddressexist.groups(1)[0]
        else:
            logging.info("Peer IP addrees not configured for peer:"+PeerName)
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
                    ISCPort = Ports.groups(1)[0]
                else:
                    UntagPorts = re.search (r"Ports.*Number.*active.*ports.*\n.*Untag:\s+(\w+).*\r",output2)
                    if UntagPorts:
                        ISCPort = UntagPorts.groups(1)[0]
                    else:
                        logging.error("No Ports found in ISC Vlan: "+ISCVlan)
            else:
                #-- Untagged ISC Vlan is given a tag of 12345
                ISCVlanID = 12345
                UntagPorts = re.search (r"Ports.*Number.*active.*ports.*\n.*Untag:\s+(\w+).*\r",output2)
                if UntagPorts:
                    ISCPort = UntagPorts.groups(1)[0]
                else:
                    logging.error("No Ports found in ISC Vlan : "+ISCVlan)
        else:
            logging.info("No Tag Info Present for ISCVlan: " + ISCVlan)
         #-- remove invalid characters from the port
        if ISCPort:
            ISCPort = ISCPort.strip('g')
    else:
        logging.error("No ISCVlan present !!!")



    #-- Add to Database
    MLAGSQL.AddMLAGPeerInstance(1,1,ISCPort,PeerName,VirtualRouter,PeerIPAddress,ISCVlan,LocalIPAddress,ISCVlanID,CheckpointStatus,Authentication,MLAGPorts)
