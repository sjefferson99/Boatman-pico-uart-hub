import machine
import json

sda1 = machine.Pin(2)
scl1 = machine.Pin(3)
i2c1 = machine.I2C(1, sda=sda1, scl=scl1, freq=100000)

print('i2c1 devices found at')
devices = i2c1.scan()
if devices:
    for i in devices:
        print(i)

i2c_lights = 0x41

print("command register config")

#10000000 Get/set config data
#10000001 Get group assignments

#01GRIIII Set LED values
#data byte LED duty cycle

group = True #(G)
reset = True #(R)
id = 0 # (IIII)
duty = 255

commandRegister = 0b00000000

if id < 16:
    print("id is good")
    commandRegister = 0b01000000 + id # Set value command

    if group:
        commandRegister = commandRegister + 0b00100000

    if reset:
        commandRegister = commandRegister + 0b00010000

else:
    print("Bad ID")

print(commandRegister)

data = []
data.append(commandRegister)
data.append(duty)

while len(data) < 8:
    data.append(0)

sendData = bytearray(data)

if i2c_lights in devices:
    i2c1.writeto(i2c_lights, sendData)

    returnData = i2c1.readfrom(i2c_lights, 1)

    print(returnData)

    returnData = int(returnData[0])
    print(returnData)

    if returnData > 0:
        if returnData & 0b00000010:
            print ("Group config out of date, reloading")
            data = []
            data.append(0b10000001)
            while len(data) < 8:
                data.append(0)
            sendData = bytearray(data)
            i2c1.writeto(i2c_lights, sendData)

            incomingBytes = i2c1.readfrom(i2c_lights, 2)
            print(incomingBytes)
            length = int.from_bytes(incomingBytes, "big")
            print(length)
            returnData = i2c1.readfrom(i2c_lights, length)
            led_groups = {}
            led_groups = json.loads(returnData)
            print(led_groups)

        else:
            print("unknown error")

    else:
        print("Successful update")

else:
    print("No valid devices")