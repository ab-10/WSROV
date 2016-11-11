def get_temp(ser):
    """ Requests and returns temperature
    
    Arguments:
    ser -- serial port object to which Master is connected
    
    Returns:
    Temperature readings from sensor on Slave in Celsius
    """

   ser.write('S')
   ser.write('S')
   ser.write('t')
   ser.write('t')
   ser.write('E')

   temp = ser.read(2)
   return temp

def get_hum(ser):
    """ Requests and returns temperature

    Arguments:
    ser -- serial port object to which Master is connected

    Returns:
    Relative humidity readings from sensor on Slave in percent
    """

    ser.write('S')
    ser.write('S')
    ser.write('h')
    ser.write('h')
    ser.write('E')

    hum = ser.read(2)
    return temp
