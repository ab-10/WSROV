#!/usr/bin/env python
import logging
import itertools
import platform
import pySerial
import time
from serial.tools import list_ports
if platform.system() == 'Windows':
    import _winreg as winreg
else:
    import glob


def build_cmd_str(cmd, args=None):
    """
    Build a command string that can be sent to the arduino.

    Input:
        cmd (str): the command to send to the arduino, must not
            contain a % character
        args (iterable): the arguments to send to the command

    @TODO: a strategy is needed to escape % characters in the args
    """
    if args:
        args = '%'.join(map(str, args))
    else:
        args = ''
    return "@{cmd}%{args}$!".format(cmd=cmd, args=args)

def get_version(sr):
    cmd_str = build_cmd_str("version")
    try:
        sr.write("A")
        sr.flush()
    except Exception:
        return None
    reading = ""
    while reading == "":
        reading = sr.readline().replace("\r\n", "")
    return reading

port = serial.Serial("/dev/ttyACM0", timeout=0.5)

print(get_version(port))
