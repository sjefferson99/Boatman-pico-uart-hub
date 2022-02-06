import machine
import json

#Deals with debug messages appropriately
def debug(message):
    #TODO Support UART output (unsure if toggle signalk/debug or put debug into signalk format)
    if debugEnable:
        print(message)

#Enables printing debug messages
global debugEnable
debugEnable = True

#Config I2C
sda1 = machine.Pin(2)
scl1 = machine.Pin(3)
i2c1_freq = 100000

# Init I2C
debug("Init I2C")
i2c1 = machine.I2C(1, sda=sda1, scl=scl1, freq=i2c1_freq)

#Scan i2C bus for devices
debug('i2c1 devices found at')
devices = i2c1.scan()
if devices:
    for i in devices:
        debug(i)

else:
    debug("No I2C devices found")

##########################
#I2C Pico light controller
##########################
i2c_lights = 0x41 #Pico lights controller I2C address
debug("Pico light controller I2c address set to: ")
debug(i2c_lights)

debug("command register config")

#10000000 Get/set config data
#10000001 Get group assignments

#01GRIIII Set LED values
#data byte LED duty cycle

group = True #(G)
reset = True #(R)
id = 1 # (IIII)
duty = 255

commandRegister = 0b00000000

if id < 16:
    debug("LED ID is good") #TODO look up LED and group IDs in config dictsto check properly
    commandRegister = 0b01000000 + id # Set value command

    if group:
        commandRegister = commandRegister + 0b00100000

    if reset:
        commandRegister = commandRegister + 0b00010000

else:
    debug("Bad ID")

debug("Command register: ")
debug(commandRegister)

data = []
data.append(commandRegister)
data.append(duty)

#Fill output buffer with 8 bytes as I2C responder reads 8 into input buffer and will load known data into the buffer where bytes < 8
while len(data) < 8:
    data.append(0)

sendData = bytearray(data)

#Check the I2C target exists
if i2c_lights in devices:
    #Send command byte and duty data
    i2c1.writeto(i2c_lights, sendData)
    #Expect one byte status return
    returnData = i2c1.readfrom(i2c_lights, 1)
    debug(returnData)
    returnData = int(returnData[0])
    debug(returnData)

    #Return code is error
    if returnData > 0:
        #Group config is potentially out of sync
        if returnData & 0b00000010:
            debug("Group config is potentially out of sync, reloading")
            #Build a reload group config command
            data = []
            data.append(0b10000001)
            #Pack spare bytes up to 8 with 0s
            while len(data) < 8:
                data.append(0)
            sendData = bytearray(data)
            i2c1.writeto(i2c_lights, sendData)
            #Expected return from group config update is number of bytes of data to be sent in 2 byte big endian format
            incomingBytes = i2c1.readfrom(i2c_lights, 2)
            debug(incomingBytes)
            length = int.from_bytes(incomingBytes, "big")
            debug(length)
            #Expects immediate send of the group config data in JSON, byte count specified above
            returnData = i2c1.readfrom(i2c_lights, length)
            debug(returnData)
            #Populate updated LED groups config data dict
            led_groups = {}
            led_groups = json.loads(returnData)
            debug(led_groups)

        else:
            #Non zero but unknown return code
            debug("unknown error")

    else:
        debug("Successful update")

else:
    debug("Target device not present on I2C bus")