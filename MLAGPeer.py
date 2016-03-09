import MLAGSQL
import logging
import connect
import Library
import re
#-- Global variables
global ISCId
ISCId = 0

def get_mlag_peer(handler,SwitchID):
    """
    This procedure collects MLAG Peer Information
    and inserts in to the table MLAGPeerInstance

    :param handler: connection handler to the switch
    :param SwitchID: Switch ID
    :return: none

    """
    #-- Global variables

    global ISCId

    #-- Initialize the local variables
    ISCVlan = ""
    VirtualRouter = ""
    CheckpointStatus = ""
    Authentication = ""
    PeerName = ""
    ISCPort = []
    ISCvlanport =""
    PeerIPAddress = ""
    LocalIPAddress= ""
    ISCVlanID = 0
    index = 0
    #-- Disable cli paging in switch
    Library.SendCmd(handler,"disable clipaging")
    #-- Get the show mlag peer output
    wholeoutput = Library.SendCmd(handler,"show mlag peer")

    #-- Parse the output for required fields to feed to MLAGPeer table
    #-- Peer Name list
    PeerNameexistlist = re.findall(r"MLAG\s+Peer\s+:\s+(.*\S+)\s+.*",wholeoutput)
    if PeerNameexistlist:
        logging.info("MLAG Peers are present")
    else:
        logging.error("No MLAG Peer Exists in Switch ID : "+str(SwitchID))
        logging.error("Returning with failure to update the MLAG Peer Instance")
        return

    #-- split the output MLAG peerwise
    outputpart = Library.split_before("MLAG\s+Peer\s+:",wholeoutput)  #-- Parse the output peerwise
    for output in list(outputpart):

        #-- Peer Name
        PeerName = re.search(r"MLAG\s+Peer\s+:\s+(.*\S+)\s+.*",output)
        if PeerName == None:
            continue
        PeerName=PeerName.groups(1)[index]

        #-- Virtual router
        VirtualRouterexist = re.search (r"Virtual\s+Router\s+:\s+(.*\S+)\s+\r",output)
        if VirtualRouterexist:
            VirtualRouter = VirtualRouterexist.groups(1)[index]

        #-- Checkpointstatus
        CheckpointStatusexist = re.search (r"Checkpoint\s+Status\s+:\s+(Up|Down)\s+.*",output)
        if CheckpointStatusexist:
            CheckpointStatus=CheckpointStatusexist.groups(1)[index]

        #-- Authentication
        Authenticationexist = re.search(r"Authentication\s+:\s+(.*\S+)\s+.*",output)
        if Authenticationexist:
            Authentication = Authenticationexist.groups(1)[index]

        #-- MLAG Ports
        match=re.search (r"MLAG.*ports\s+:\s+([1-9]+)\s+.*",output)
        if match:
            MLAGPorts = int(match.groups(1)[index])
        else:
            MLAGPorts = 0
            logging.error("No MLAG ports present")

        #-- ISC vlan
        ISCVlanpresent = re.search (r"VLAN\s+:\s+(.*\S+)\s+Virtual.*Router.*",output)
        if ISCVlanpresent:
            ISCId = ISCId + 1
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
                    Ports = re.search(r"Tag:\s+[\*|!]?(\d?:?\d+g?).*\r",output2)
                    if Ports:
                        ISCPort.append(Ports.groups(1)[0])
                    UntagPorts = re.search (r"Untag:\s+[\*|!]?(\d?:?\d+g?).*\r",output2)
                    if UntagPorts:
                        ISCPort.append(UntagPorts.groups(1)[0])

                else:
                    ISCVlanID =re.search(r"Tagging.*Untagged.*Internal.*tag\s+(\d+).*",output2)
                    if ISCVlanID:
                        ISCVlanID =ISCVlanID.groups(1)[0]
                    UntagPorts = re.search (r"Untag:\s+[\*|!]?(\d?:?\d+g?).*\r",output2)
                    if UntagPorts:
                        ISCPort.append(UntagPorts.groups(1)[0])

            else:
                logging.info("No Tag Info Present for ISCVlan: " + ISCVlan)
            #-- get the ISC Port
            ISCPortlength = len(ISCPort)
            if ISCPortlength:
                ISCvlanport = ISCPort[0]
                logging.info(ISCPort)
                if ISCPortlength > 1:
                    logging.error("Number of ports present in ISC vlan is "+str(ISCPortlength)+ "!!!!")
                    logging.info("Go for the trunked port if exists as ISC Port since it is most configured ")
                    for port in ISCPort:
                        match = re.search(r".*g",port)
                        if match:
                           ISCvlanport = port.strip('g')
                           break
            else :
                logging.error("No Ports found in ISC Vlan : "+ISCVlan)
        else:
            logging.error("No ISCVlan present !!!")
        if ISCvlanport:
            ISCvlanport = str(ISCvlanport.strip('g'))
        #-- Add to Database
        MLAGSQL.AddMLAGPeerInstance(SwitchID,ISCId,ISCvlanport,PeerName,VirtualRouter,PeerIPAddress,ISCVlan,LocalIPAddress,ISCVlanID,CheckpointStatus,Authentication,MLAGPorts)

