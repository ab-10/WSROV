import usb.core
import usb.util

if usb.core.find(bDeviceClass=7) is None:
    print("no printer found")
