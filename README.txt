== mLAG Diag Tool ==
Requires Python: 2.7
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
   - MLAGPeer.py
 
== Installation ==
1. Extract the downloaded tar file (MLAGDiag.tar)
2. Execute the file "main.py"

== Example ==

-bash-4.2$ python main.py
DISCLAIMER:
This Program is to diagnose the MLAG Configuration between peers
This Program does not make any changes to any switch configuration
It is free software and it comes without any Warranty


Please Enter Number of MLAG Switches to Debug: 2
Please Enter IP Address of switch 1: 10.127.11.28
Please Enter UserName of Switch 1: admin
Please Enter Password of Switch 1:

!!!Connecting to the Switch 1. Please Wait!!!

Connecting in 3 Seconds ...

Please Enter IP Address of switch 2: 10.127.11.30
Please Enter UserName of Switch 2: admin
Please Enter Password of Switch 2:

!!!Connecting to the Switch 2. Please Wait!!!

Connecting in 3 Seconds ...

[] Diag: Getting MLAG Peer Configuration for 10.127.11.28 ..

[] Diag: Getting MLAG Peer Configuration for 10.127.11.30 ..

[] Diag: Getting MLAG Port Configuration for the Switch 10.127.11.28 ..

[] Diag: Getting MLAG Port Configuration for the Switch 10.127.11.30 ..

[] Diag: Validating MLAG Peer Status
	TEST: To validate MLAG Check-Point, Auth & MLAG ports Status
	PASS: Check-Point Status is UP between peers
	PASS: The Auth method of Peer 1 and Peer 2 are same
	PASS: The number of MLAG ports of Peer 1 and Peer 2 are same

[] Diag: PEER1 VLAN Check Between ISC and MLAG ID
	TEST: Check VLAN between ISC Port : 20 & MLAGID: 111, MLAG Port: 19
	PASS: ISC Port is associated in all MLAG VLAN(s)

[] Diag: PEER2 VLAN Check Between ISC and MLAG ID
	TEST: Check VLAN between ISC Port : 5:20 & MLAGID: 111, MLAG Port: 5:19
	PASS: ISC Port is associated in all MLAG VLAN(s)

[] Diag: VLAN and MLAG ID Comparisons Between MLAG Peers
	TEST: To validate MLAG IDs between Peers
	PASS: MLAG ID between Peers 10.127.11.28 and 10.127.11.30 are same

	TEST: Checking ISC VLAN Configuration between Peers 10.127.11.28 and 10.127.11.30
	PASS: ISC VLAN between peers 10.127.11.28 and 10.127.11.30 are same

	TEST: Checking MLAG VLAN Configurations Between Peers 10.127.11.28 and 10.127.11.30 for MLAG ID 111
	PASS: MLAG VLAN between Peers 10.127.11.28 and 10.127.11.30 for MLAG ID 111 are same

Diag Completed!




