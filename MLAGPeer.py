import MLAGSQL
import logging
import connect
import Library
import re
import sys
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
    #-- local variable
    failure =0

    #-- Test start
    print ("[] Diag: Getting MLAG Peer Configuration for %s .." %(connect.SwitchID_switchInfo[SwitchID][0]))

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

        print("\tFAIL: No MLAG Peer Exists in Switch:")
        connect.DisplaySwitchInfo(SwitchID)
        connect.Closeconnectiontoswitches()
        sys.exit()

    #-- split the output MLAG peerwise
    outputpart = Library.split_before("MLAG\s+Peer\s+:",wholeoutput)
    #-- Parse the output peerwise
    for output in list(outputpart):
        #-- Initialize the local variables
        VirtualRouter = ""
        CheckpointStatus = ""
        Authentication = ""
        PeerName = ""
        ISCPort = []
        ISCvlanport =""
        PeerIPAddress = ""
        LocalIPAddress= ""
        ISCVlanID = 0

        #-- Peer Name
        PeerName = re.search(r"MLAG\s+Peer\s+:\s+(.*\S+)\s+.*",output)
        if PeerName == None:
            continue
        PeerName=PeerName.groups(1)[0]

        #-- Virtual router
        VirtualRouterexist = re.search (r"Virtual\s+Router\s+:\s+(.*\S+)\s+\r",output)
        if VirtualRouterexist:
            VirtualRouter = VirtualRouterexist.groups(1)[0]

        #-- Checkpointstatus
        CheckpointStatusexist = re.search (r"Checkpoint\s+Status\s+:\s+(Up|Down)\s+.*",output)
        if CheckpointStatusexist:
            CheckpointStatus=CheckpointStatusexist.groups(1)[0]

        #-- Authentication
        Authenticationexist = re.search(r"Authentication\s+:\s+(.*\S+)\s+.*",output)
        if Authenticationexist:
            Authentication = Authenticationexist.groups(1)[0]

        #-- MLAG Ports
        match=re.search (r"MLAG.*ports\s+:\s+([1-9]+)\s+.*",output)
        if match:
            MLAGPorts = int(match.groups(1)[0])
        else:
            MLAGPorts = 0
            failure = failure + 1
            print("\tERROR:No MLAG ports present for Peer "+str(PeerName))
            continue

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
                #-- Tagged vlan ports check
                if Tagged:
                    ISCVlanID = Tagged.groups(1)[0]
                    #-- tagged ports
                    output3=re.search(r"(Tag:.*\r)",output2)
                    if output3:
                        output3=''.join(output3.groups(1)[0])
                        Ports = re.findall(r"[\*|!]?(\d?:?\d+g?)",output3)
                        if Ports:
                            ISCPort.extend(Ports)
                    #--Untagged ports
                    output3=re.search(r"(Untag:.*\r)",output2)
                    if output3:
                        output3=''.join(output3.groups(1)[0])
                        Ports = re.findall(r"[\*|!]?(\d?:?\d+g?)",output3)
                        if Ports:
                            ISCPort.extend(Ports)
                else:
                    ISCVlanID =re.search(r"Tagging.*Untagged.*Internal.*tag\s+(\d+).*",output2)
                    if ISCVlanID:
                        ISCVlanID =ISCVlanID.groups(1)[0]
                    output3=re.search(r"(Untag:.*\r)",output2)
                    if output3:
                        output3=''.join(output3.groups(1)[0])
                        Ports = re.findall(r"[\*|!]?(\d?:?\d+g?)",output3)
                        if Ports:
                            ISCPort.extend(Ports)
            else:
                logging.info("No Tag Info Present for ISCVlan: " + ISCVlan)
            #-- get the ISC Port
            ISCPortlength = len(ISCPort)
            if ISCPortlength:
                ISCvlanport = ISCPort[0]
                if ISCPortlength > 1:
                    print("\tERROR: Number of ports present in ISC vlan "+str(ISCVlan)+" = "+str(ISCPortlength))
                    failure = failure + 1
                    continue

            else :
                print("\tERROR: No Ports found in ISC Vlan : "+ISCVlan+" for Peer "+PeerName)
                failure = failure + 1
                continue

        else:
            print("\tERROR: No ISCVlan present for Peer "+PeerName)
            failure = failure + 1
            continue
        if ISCvlanport:
            ISCvlanport = str(ISCvlanport.strip('g'))
        #-- Add to Database
        MLAGSQL.AddMLAGPeerInstance(SwitchID,ISCId,ISCvlanport,PeerName,VirtualRouter,PeerIPAddress,ISCVlan,LocalIPAddress,ISCVlanID,CheckpointStatus,Authentication,MLAGPorts)
    if failure:
        logging.info("\tFAIL:Getting MLAG Peer Configuration")
    else:
        logging.info("\tPASS: Getting MLAG Peer Configuration")
    # Print New Line
    print ("")