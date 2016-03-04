import connect
import sys
import socket
#from connect import sHandler



IPAddress = raw_input ("\nPlease Enter your Management IP Address: ")
try:
	socket.inet_aton(IPAddress)
except socket.error:
	print "\n!!! Error: Please Enter Valid IP Address !!!\n"
	sys.exit()

username = raw_input("Enter your Username: ")
password = raw_input("Enter your Password: ")
retHandler = Connect(IPAddress,username,password)
#from connect import sHandler
print retHandler
