import MLAGSQL
import logging
logging.basicConfig(level=logging.INFO)
import sys


def CompareVlansBetween(ISCPortVLAN, MLAGPortVLAN):

    ISCPortVLAN.sort()
    MLAGPortVLAN.sort()

    isc_vlan =set(MLAGPortVLAN).difference(ISCPortVLAN)
    if isc_vlan:
    	sys.stdout.write ("\tFAIL: ISC Port is not associated with the MLAG VLAN ")
        print (isc_vlan)
    else:
	print ("\tPASS: ISC Port is associated in all MLAG VLAN(s)")
    print ("")

def VlanCheck():

    global c
    c=MLAGSQL.c
    ISCPortVLAN=[]
    MLAGPortVLAN=[]

    ''' Loop-1: Get SWID from the table '''
    GetSwId=c.execute("SELECT DISTINCT SwitchID FROM PortInfo")
    for SwID in GetSwId.fetchall():
        SwID=SwID[0]
        print("[] Diag: PEER%s VLAN Check Between ISC and MLAG ID" % SwID)

        ''' Loop-1.1: Go by ISC ID from Table '''
        result=c.execute("SELECT DISTINCT ISCID FROM PortInfo WHERE SwitchID='%s';" %(SwID))
        for isc_id in result.fetchall():
            ''' Loop-1.1.1: Get ISC Port ID from table '''
            res=c.execute("SELECT DISTINCT PortID FROM PortInfo WHERE SwitchID='%s' AND ISCID='%s' AND MLAGID=0;" % (SwID, isc_id[0]))
            for isc_pid in res.fetchall():

                ''' Loop-1.1.1.1: populate ISCPortVLAN List'''
                vlantag=c.execute("SELECT VlanTag FROM PortInfo WHERE SwitchID='%s' AND ISCID='%s' AND MLAGID=0 AND PortID='%s';" % (SwID, isc_id[0], isc_pid[0]))
                for vlan in vlantag.fetchall():
                    ISCPortVLAN.append(vlan[0])

                ''' Loop-1.1.1.2: Get MLAG Port ID '''
                mlag=c.execute("SELECT DISTINCT PortID FROM PortInfo WHERE SwitchID='%s' AND ISCID='%s' AND MLAGID !='0';" %(SwID, isc_id[0]))
                for mlag_pid in mlag.fetchall():

                    ''' Loop-1.1.1.2.1: Populate MLAGPortVLAN List '''
                    mlag_vlan=c.execute("SELECT VlanTag FROM PortInfo WHERE SwitchID='%s' AND ISCID='%s' AND PortID='%s';" %(SwID, isc_id[0], mlag_pid[0]))
                    for mlag_vid in mlag_vlan.fetchall():
                        MLAGPortVLAN.append(mlag_vid[0])

                    id=c.execute("SELECT DISTINCT MLAGID FROM PortInfo WHERE SwitchID='%s' AND ISCID='%s' AND PortID='%s';" %(SwID, isc_id[0], mlag_pid[0]))
                    mlag_id=id.fetchall()[0]

                    ''' Compare ISC VLAN LIST with Each MLAG ID VLAN LIST '''
                    print("\tTEST: Check VLAN between ISC Port : %s & MLAGID: %s, MLAG Port: %s" %(isc_pid[0], mlag_id[0], mlag_pid[0]))
                    CompareVlansBetween(ISCPortVLAN, MLAGPortVLAN)

                    ''' Clear MLAGPortVLAN List and go to Loop-1.1.1.2 '''
                    try:
                        MLAGPortVLAN.clear()
                    except:
                        MLAGPortVLAN=[]

                ''' Clear ISCPortVLAN list and go to Loop-1.1.1 '''
                try:
                    ISCPortVLAN.clear()
                except:
                    ISCPortVLAN=[]
