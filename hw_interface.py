"""
helpful sys commands:

detect i2c bus connected devices
`
i2cdetect -y 1
`

read from address
`
i2cget -y 1 0x38
`
"""


import smbus

bus = smbus.SMBus(1)

buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mux_l = 0
mux_r = 0

def getButtonState():
	buf = bus.read_byte(0x20)
	
	buttons[5] = 1 - ((buf >> 7) & 1)
	buttons[6] = 1 - ((buf >> 6) & 1)
	
	if (buf >> 5) & 1 == 0:
		mux_r = 3
	elif (buf >> 4) & 1 == 0:
		mux_r = 2
	elif (buf >> 3) & 1 == 0:
		mux_r = 1
	else:
		mux_r = 0
		
	if (buf >> 2) & 1 == 0:
		mux_l = 3
	elif (buf >> 1) & 1 == 0:
		mux_l = 2
	elif (buf >> 0) & 1 == 0:
		mux_l = 1
	else:
		mux_l = 0
	
	buf = bus.read_byte(0x21)
	
	buttons[4] = 1 - ((buf >> 7) & 1)
	buttons[3] = 1 - ((buf >> 6) & 1)
	buttons[2] = 1 - ((buf >> 5) & 1)
	buttons[1] = 1 - ((buf >> 4) & 1)
	buttons[0] = 1 - ((buf >> 3) & 1)
	buttons[9] = 1 - ((buf >> 2) & 1)
	buttons[8] = 1 - ((buf >> 1) & 1)
	buttons[7] = 1 - ((buf >> 0) & 1)
	
	
	return {"/wheel/buttons": buttons, "/wheel/mux_l": mux_l, "/wheel/mux_r": mux_r}


import socket
import json
import time


data = {"method": "set", "data": {}}

def startConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.20.22.1", 2400))
    return s

s = startConnection()

while True:
    data["data"] = getButtonState()

    try:
        s.send(json.dumps(data).encode())
    except ConnectionResetError or ConnectionRefusedError as e:
        print(e)
        s.close()
        s = startConnection()

    print(data)
    time.sleep(0.1)
