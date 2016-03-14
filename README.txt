== mLAG Diag Tool ==
Requires Pythont: 2.7
License: Free Diag Tool for EXOS Mlag configuration

== Description ==
This is a free software to diag EXOS MLAG mis-configuration between peers. This has been tested in Python 2.7 version.
You can checkout the project files from  https://github.com/ndprasad09/MLAGDiag

== Requirement ==
 * Operating system: Linux/Win with Python2.7
 * Library files that comes with the software
   - connect.py
   - ValidationLib.py
   - MLAGSQL.py
   - MLAGPorts.py
   - Library.py
   - vLanCheck.py
   - interVLANCheck.py
 
== Installation ==
1. Extract the downloaded tar file (MLAGDiag.tar)
2. Execute the file "main.py"

== Example ==

-bash-4.2$ python main.py
Please Enter Number of MLAG Switches to Debug: 2
Please Enter IP Address of switch 1: 10.127.11.21
Please Enter UserName of Switch 1: admin
Please Enter Password of Switch 1:

!!!Connecting to the Switch 1. Please Wait!!!

Connecting in 3 Seconds
...
!!!!Connection Successfull!!!

Please Enter IP Address of switch 2: 10.127.11.28
Please Enter UserName of Switch 2: admin
Please Enter Password of Switch 2:

!!!Connecting to the Switch 2. Please Wait!!!

Connecting in 3 Seconds
...
!!!!Connection Successfull!!!

[] Diag: Checkpointing
	TEST: Check checkpinting between peers
	PASS: The Auth method of Peer 1 and Peer 2 are the same
	PASS: The number of MLAG ports of Peer 1 and Peer 2 are the same

[] Diag: PEER1 VLAN Check Between ISC and MLAG ID
        TEST: Check VLAN between ISC Port : 1:20 & MLAGID: 111, MLAG Port: 1:1
        PASS: ISC Port is associated in all MLAG VLAN(s)

[] Diag: PEER2 VLAN Check Between ISC and MLAG ID
        TEST: Check VLAN between ISC Port : 20 & MLAGID: 222, MLAG Port: 5
        PASS: ISC Port is associated in all MLAG VLAN(s)

[] Diag: VLAN config between Peers 1 and 2
	FAIL: MLAG ID 111 is not Present in SwitchID 2
	FAIL: MLAG ID 222 is not Present in SwitchID 1

Diag Completed !




