""" sends data to Master using simple com protocol
"""
def send(port, type, byte1='!', byte2='!', byte3='!', byte4='!'):
    msg = type + byte1 + byte2 + byte3 + byte4 + 'E'
    port.write(msg.encode('ascii'))
    port.flush()

""" reads from Master
"""
def read(port):
    reading = ""
    while reading == "":
        reading = sr.readline().replace(b"\r\n", b"")
    return reading
