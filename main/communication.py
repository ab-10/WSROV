""" Handles communication with the robot
"""
def send(port, type, byte1='!', byte2='!', byte3='!', byte4='!'):
    port.write(type)
    port.write(byte1)
    port.write(byte2)
    port.write(byte3)
    port.write(byte4)
    port.write('E')
