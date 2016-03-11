import MLAGSQL
import logging
import launch
logging.basicConfig(level=logging.INFO)
import sqlite3
import sys


def CompareVlansBetween(ISCPortVLAN, MLAGPortVLAN):

    ISCPortVLAN.sort()
    MLAGPortVLAN.sort()

    if MLAGPortVLAN == ISCPortVLAN:
        print("PASS: ISC Port VLAN & MLAG Port VLAN matched")
    else:
        #print("FAIL: ISC Port VLAN & MLAG Port VLAN mis-match")
        print("FAIL:")
        mlag_vlan=set(ISCPortVLAN).difference(MLAGPortVLAN)
        isc_vlan =set(MLAGPortVLAN).difference(ISCPortVLAN)
        if mlag_vlan:
            sys.stdout.write ("MLAG Port is not associated with the VLAN(s):")
            print (mlag_vlan)
        if isc_vlan:
            sys.stdout.write ("ISC Port is not associated with the VLAN(s):")
            print (isc_vlan)

def VlanCheck():

    global c
    c=MLAGSQL.c
    ISCPortVLAN=[]
    MLAGPortVLAN=[]

    GetSwId=c.execute("SELECT DISTINCT SwitchID FROM PortInfo")
    for SwID in GetSwId.fetchall():
        SwID=SwID[0]
        print("\nPEER%s: VLAN Check Between ISC and MLAG ID" % SwID)
        ''' Get ISCID from the Switch '''
        result=c.execute("SELECT DISTINCT ISCID FROM PortInfo WHERE SwitchID=%s;" %(SwID))
        ''' Get ISC Port VlanTag List '''
        for isc_id in result.fetchall():
            res=c.execute("SELECT VlanTag FROM PortInfo WHERE SwitchID=%s AND ISCID=%s AND MLAGID=0;" % (SwID, isc_id[0]))
            for val in res.fetchall():
                ISCPortVLAN.append(val[0])

                ''' Get List of MLAGID for each ISC '''
                res=c.execute("SELECT DISTINCT MLAGID FROM PortInfo WHERE SwitchID=%s AND ISCID=%s AND MLAGID !='0';" %(SwID, isc_id[0]))
                ''' Get VLAN List for each MLAG ID '''
                for mlag_id in res.fetchall():
                    res=c.execute("SELECT VlanTag FROM PortInfo WHERE SwitchID=%s AND ISCID=%s AND MLAGID='%s';" %(SwID, isc_id[0], mlag_id[0]))
                    for val in res.fetchall():
                        MLAGPortVLAN.append(val[0])
                    ''' Compare ISC VLAN LIST with Each MLAG ID VLAN LIST '''
                    print("\nTEST: Check VLAN between ISC ID : %s & MLAG ID: %s" %(isc_id[0], mlag_id[0]))
                    CompareVlansBetween(ISCPortVLAN, MLAGPortVLAN)
                    MLAGPortVLAN.clear()
                ISCPortVLAN.clear()

