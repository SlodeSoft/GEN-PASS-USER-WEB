from pykeepass import PyKeePass
import base64

# load database


class SECRET:
    def __init__(self, tonkdbx, lepassdukdbx, tongroup, tontitle):
        # DECODE 64 VARIABLE ENTRY
        addallvarlist = list()
        decodeallvarlist = list()
        addallvarlist.extend([tonkdbx,
                              lepassdukdbx,
                              tongroup,
                              tontitle])
        for x in addallvarlist:
            base64_message = x
            base64_bytes = base64_message.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            decodeallvarlist.append(message)
        # READ KEEPASS
        __kp__ = PyKeePass(decodeallvarlist[0], password=decodeallvarlist[1])
        # Find any group by its name
        __group__ = __kp__.find_groups(name=decodeallvarlist[2], first=True)
        self.__entry__ = __kp__.find_entries(title=decodeallvarlist[3], first=True)


# INIT VARIABLES
KDBX_VAR = "QzpcXFVzZXJzXFxhZG1pbi4wMDBcXFB5Y2hhcm1Qcm9qZWN0c1xcU0FOREJPWFxcU0VDUkVULmtkYng="
KDBXPASS_VAR = "WlBVeDhERGYqSnJFJjlOWnJkSnlzbmVqNEpeQTckZ0Zl"
KDBXGRP_VAR = "R2luZ0xVQ0hFckVHT1RPUkFUcmVNTmFWQVRJQ0lhTnRBZ29kSUNSVWNUSUNrTk91clQ="


# GET PASSWORD HOST USER, DB,...
__un__ = SECRET(KDBX_VAR, KDBXPASS_VAR, KDBXGRP_VAR,
                "QXRlQXRFTWluVklTeUtFVGVydk9MeXNJTHRVUmVUSUNlT25nRU5PdXNIVXRFTlNpVU0=")
__deux__ = SECRET(KDBX_VAR, KDBXPASS_VAR, KDBXGRP_VAR,
                  "QWNpQmxhZHZFbnRBVmVOYmVEdXNFbW9uZWxlbU9sZVRlcm5pbkVZRWdNYW5EQVRFUkM=")
__trois__ = SECRET(KDBX_VAR, KDBXPASS_VAR, KDBXGRP_VAR,
                   "cEF0RE91dFNDb21hVHJpU0NyRXNJbmF0RXJEaVZJbmVJa2F0aWZMWUVycGhZZFJvcGw=")
