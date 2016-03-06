import socket
import re
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