import serial
import time

port = serial.Serial("COM4", timeout = 10)

time.sleep(2) #Waits so the port is initialized

port.write(b'54')
