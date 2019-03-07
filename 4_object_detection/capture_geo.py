# coding: utf-8

from dronekit import connect, VehicleMode
vehicle = connect('192.168.0.9:14550', wait_ready = False)
vehicle.wait_ready = ('autopilot_version')
coord = vehicle.location.global_frame
print(coord)
with open('coord.txt', 'a') as f:
    #for i, line in enumerate(fp):
    #if '\xe2' not in line:
    f.write(str(coord))

'''
f = open(“coord.txt”) 
f.write(str(coord))
f.close()
'''

