import time

""" sends data to Master using simple com protocol
"""
def send(port, type, byte1='!', byte2='!', byte3='!', byte4='!'):
    msg = type + str(byte1) + str(byte2) + str(byte3) + str(byte4) + 'E'
    port.write(msg.encode('ascii'))
    port.flush()

""" reads from Master
"""
def read(port):
    time = time.time()
    reading = b""
    while (reading == b"") and (time() - time < 2):
        reading = port.readline().replace(b"\r\n", b"")
    return reading
