import serial
import json

ser = serial.Serial('/dev/ttyUSB0',115200)

while True:

    line = ser.readline().decode().strip()

    try:
        data = json.loads(line)

        print(data)

    except:
        pass