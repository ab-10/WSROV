import communication

def get_temp(port):
    """ Requests and returns temperature

    Arguments:
    ser -- serial port object to which Master is connected

    Returns:
    Temperature readings from sensor on Slave in Celsius
    """

    communication.send(port, 'S', 't')

    temp = communication.read(port)
    return temp

def get_hum(port):
    """ Requests and returns temperature

    Arguments:
    ser -- serial port object to which Master is connected

    Returns:
    Relative humidity readings from sensor on Slave in percent
    """

    communication.send(port, 'S', 'h')

    hum = communication.read(port)
    return hum
