# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 14:06:12 2015

@author: Gaurav Mukherjee
"""

import bluetooth

target_name = "EMG"
target_address = None
#bdaddr = 'M13762'

nearby_devices = bluetooth.discover_devices()

print "the nearby devices are: ", nearby_devices

for bdaddr in nearby_devices:
    #if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"
