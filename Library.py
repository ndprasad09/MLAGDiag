import socket
import re
import os
import sys
import time

def SendCmd (sHandler,command):
        """
        SendCmd procedure takes a cli command as input and execute
        it in the switch CLI and returns the output as string
        """
        returnstring = ""
        Flag = 0
        #time.sleep(1)
        try:
            if sHandler != 0:
                sHandler.write (command +"\n")
                retStr = sHandler.read_until(command)
                #print retStr

        except:
            print ("ERROR: There seems to be connectivity issue. Please Retry !!!")
            sys.exit()

        else:
            match = re.search(""+command+"",retStr)
            if not match:
                #print ("ERROR: Command %s not executed properly.There might be connection issue. Exiting the Script" %(command))
                Flag = 1
                #sys.exit()
            else:
                try:
                    returnstring = sHandler.read_until("#",timeout=100) #Timeout for Slow Connection
                    match = re.search(r".*#",returnstring)
                    if not match:
                        print ("ERROR: There seems to be some connectivity issue. Please Retry !!!")
                        sys.exit()
                except:
                    print ("ERROR: There seems to be connectivity issue. Please Retry !!!")
                    sys.exit()
                if len(returnstring) != 0:
                    #print retStr+returnstring
                    return retStr + returnstring
                else:
                    Flag  = 1
                #print ("ERROR: Command %s not executed" %(command))

            if Flag:
                print ("ERROR: Command %s not executed properly.There might be connection issue. Exiting the Script" %(command))
                sys.exit()




def split_before(pattern,text):
    """
    this proc will split the text before the
    occurance of the specified pattern
    :param pattern:
    :param text:
    :return: list of substrings
    """
    prev = 0
    for m in re.finditer(pattern,text):
        yield text[prev:m.start()]
        prev = m.start()
    yield text[prev:]


def print_error(Error_Logs):
    FG_RED= "\033[31m"
    RESET = "\033[0m"
    os_name = os.name
    if os_name == "nt":
        os.system('color 4')
        for eachLine in range(0,len(Error_Logs)):
            print (Error_Logs[eachLine])
        os.system('color 7')
    elif os_name == "posix":
        for eachLine in range(0,len(Error_Logs)):
            print (FG_RED,eachLine,RESET)

    else:
        for eachLine in range(0,len(Error_Logs)):
            print (FG_RED,eachLine,RESET)



def print_ok(Pass_Logs):
    FG_GREEN= "\033[32m"
    RESET = "\033[0m"
    os_name = os.name
    if os_name == "nt":
        os.system('color 2')
        for eachLine in range(0,len(Pass_Logs)):
            print (Pass_Logs[eachLine])
        os.system('color 7')
    elif os_name == "posix":
        for eachLine in range(0,len(Pass_Logs)):
            print (FG_GREEN,eachLine,RESET)

    else:
        for eachLine in range(0,len(Pass_Logs)):
            print (FG_GREEN,eachLine,RESET)