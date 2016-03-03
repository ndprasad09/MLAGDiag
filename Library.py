import socket
def SendCmd (sHandler,command):
        """
        SendCmd procedure takes a cli command as input and execute
        it in the switch CLI and returns the output as string
        """
        returnstring = ""
        try:
            if sHandler != 0:
                sHandler.write (command +"\n")
                returnstring = sHandler.read_until("#")
                return returnstring
        except socket.error:
            return returnstring

