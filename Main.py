import connect
import sys
import time,re
import Library
import socket


import getpass

global switchIDList
global switchInfo
global connHandler
global IPList
switchIDList = []
switchInfo = []
connHandler = []


def main():
    global switchIDList
    global switchInfo
    switchNum = raw_input("Please Enter Number of MLAG Switches to Debug: ")
    switchNum = int(switchNum)
    for eachSwitch in range(switchNum):
        tempSwitch = []
        eachSwitch = eachSwitch + 1
        while True:
            switchIP = raw_input('Please Enter IP Address of switch %d: ' % eachSwitch)
            try:
                socket.inet_aton(switchIP)
                break
            except socket.error:
                print "!!!IP address Entered is Invalid!!!"
                continue
        tempSwitch.append(eachSwitch)
        tempSwitch.append(switchIP)
        switchIDList.append(eachSwitch)
        switchInfo.append(tempSwitch)

        while True:
            username = raw_input('Please Enter UserName of Switch %d: ' % eachSwitch)
            # password = getpass.getpass (prompt = 'Enter your Password of Switch: ')
            password = raw_input('Please Enter Password of Switch %d: ' % eachSwitch)
            print "\n!!!Connecting to the Switch %d. Please Wait!!!" % eachSwitch

            retVal = connect.Connect(switchIP, username, password)
            Library.SendCmd(retVal,"disable clipaging")
            if retVal == -1:
                continue
            elif retVal == -2:
                print "!!!Connection Timeout for Switch %d. Exiting the Script!!!" % eachSwitch
                sys.exit(1)
            else:
                connHandler.append(retVal)
                break


def constructCFG ():
    global switchIDList
    global connHandler
    global SwitchMACList
    global MainList
    MainList  = []
    ISCIDList = []

    for i in range(0,len(connHandler)):
        Library.SendCmd(connHandler[i],"disable clipaging")
        retString = Library.SendCmd(connHandler[i],"show mlag peer")
        retString  = retString.strip("show mlag peer").strip()
        retString = retString.strip("Multi-switch Link Aggregation Peers:").strip()

        retVal = re.split(r'(MLAG\s+Peer)',retString,re.MULTILINE)
        retVal.remove('')
        Count  = 0
        evaluateList = []
        for j in range(0,len(retVal)/2):
            stringCat = retVal[Count] + retVal[Count+1]
            evaluateList.append(stringCat)
            Count = Count + 2



        for j in range(0,len(evaluateList)):
            match = re.search(r"Peer\s+MAC\s+:\s+(.*)\n",evaluateList[j])
            if match:
                Peer_Mac = match.groups(1)[0].strip('\r').upper()
                print Peer_Mac
                for eachItem in range(0,len(SwitchMACList)):
                    tempList = []
                    Flag = 0
                    tempList = SwitchMACList[eachItem]
                    Local_Mac = tempList[1]
                    if Peer_Mac == Local_Mac:
                        tempList1 =[]
                        tempList1.append(i+1)
                        tempList1.append(tempList[0])
                        tempList1.sort()

                        if len(MainList)!= 0:

                            for k in range(0,len(MainList)):#Checking for Entry Already Exists for Switch Pair;If Entry Exists FlAG IS SET
                                List = MainList[k]
                                if List[0] == tempList1[0] and List[1] == tempList1[1]:
                                    Flag =1
                            if Flag == 0:
                                value = int(SwitchMACList[i][1].split(':')[5],16)
                                while True:
                                    if value in ISCIDList:
                                        value = value+1
                                    else:
                                        break
                                    tempList1.append(value)
                                    MainList.append(tempList1)
                                    ISCIDList.append(value)

                                    break
                                else:
                                    tempList1.append(value)
                                    MainList.append(tempList1)
                                    ISCIDList.append(value)
                                    break

                        else:
                            value = int(SwitchMACList[i][1].split(':')[5],16)
                            tempList1.append(value)
                            MainList.append(tempList1)
                            ISCIDList.append(value)




    SwitchPairList = MainList
    return SwitchPairList


def initializeMACPair ():
    global switchIDList
    global connHandler
    global SwitchMACList
    MACList = []
    SwitchMACList = []
    for i in range(0,len(connHandler)):

        retString = Library.SendCmd(connHandler[i],"show switch")
        match = re.search(r'System\s+MAC:\s+(.*)\n',retString)
        if match:
            SwitchMAC = match.groups(1)[0].strip('\r')
            MACList.append(SwitchMAC)
            tempList = []
            tempList.append(i+1)
            tempList.append(SwitchMAC)
            SwitchMACList.append(tempList)

    print SwitchMACList

if __name__ == "__main__":
    main()
    initializeMACPair()
    constructCFG()

