import socket
import re
import os
def SendCmd (sHandler,command):
        """
        SendCmd procedure takes a cli command as input and execute
        it in the switch CLI and returns the output as string
        """
        returnstring = ""
        try:
            if sHandler != 0:
                sHandler.write (command +"\n")
                returnstring = sHandler.read_until("#",timeout=5)
                return returnstring
        except:
            return returnstring

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