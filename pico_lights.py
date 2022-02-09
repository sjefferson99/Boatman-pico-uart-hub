###########################
# I2C Pico light controller
###########################
#
# Command protocol:
#
# 0b01GRIIII 0bDDDDDDDD (6 bytes of 0) - set light or light group duty cycle
# G: 1 = Group, 0 = Individual light
# R: 1 = Reset other lights to duty cyle of 0, 0 = update only this target
# IIII = 4 bit Light or Group ID
# DDDDDDDD = 0-255 Duty cycle value 0 = off, 255 = fully on
#
# 0b1xxxxxxx: Get/set config data
# 0b10000001: Get module ID - Pico lights should return 0b00000010
# 0b10000010: Get version
# 0b10000011: Get group assignments

from machine import I2C
from time import sleep_ms
import json

class pico_light_controller:
    
    def __init__(self, I2Ccontroller: I2C, address: int = 0x41) -> None:
        self.i2c1 = I2Ccontroller
        self.I2C_address = address
        self.version = str("0.1")
        self.moduleID = 0b00000010
        self.led_groups = {}
        self.set_light_bits = 0b01000000
        self.group_bit = 0b00100000
        self.reset_bit = 0b00010000        

    def send_data(self, data: list):
        
        while len(data) < 8:
            data.append(0)

        sendData = bytearray(data)
        self.i2c1.writeto(self.I2C_address, sendData)

    def get_module_id(self) -> int:
        command_byte = 0b10000001
        data = []
        data.append(command_byte)
        self.send_data(data)        
        #Expect one byte status return
        returnData = self.i2c1.readfrom(self.I2C_address, 1)
        returnData = int(returnData[0])
        return returnData
    
    def get_version(self) -> str:
        command_byte = 0b10000010
        data = []
        data.append(command_byte)
        self.send_data(data)        
        #Expect 3 byte status return
        returnData = self.i2c1.readfrom(self.I2C_address, 3)
        returnData = returnData.decode('ansi')
        return returnData

    def check_bus(self) -> bool:
        #Is device at this address
        devices = self.i2c1.scan()
        if self.I2C_address in devices:
            #Confirm matching module ID
            if self.get_module_id() == self.moduleID:
                return True
            else:
                return False
        else:
            return False

    def get_groups(self) -> dict:
        command_byte = 0b10000011
        data = []
        data.append(command_byte)
        self.send_data(data)    
        #Expect 2 byte length data return
        returnData = self.i2c1.readfrom(self.I2C_address, 2)
        length = int.from_bytes(returnData, "big")
        #Expects immediate send of the group config data in JSON, byte count specified above
        returnData = self.i2c1.readfrom(self.I2C_address, length)
        #Populate updated LED groups config data dict
        led_groups = {}
        led_groups = json.loads(returnData)
        return led_groups

    def set_light(self, reset: bool, id: int, duty: int) -> int:
        """
        reset: true = set all other lights off and apply this light configuration only
        id: 4 bit (0-15) ID of the light to configure
        duty: 16 bit (0-255) duty for the light PWM fader, 0=off, 255=fully on
        Returns 0 on success or error code
        
        Error codes:
        -1: Command not recognised by pico_lights module
        -10: Light ID out of range
        -20: Duty value out of range
        """
        if id >=0 and id <=15:
            command_byte = self.set_light_bits + id
        else:
            return -10 #Light ID out of range
        if reset:
            command_byte += self.reset_bit
        data = []
        data.append(command_byte)
        data.append(duty)
        self.send_data(data)        
        #Expect 1 byte status return
        returnData = self.i2c1.readfrom(self.I2C_address, 1)
        return int.from_bytes(returnData, "big") * -1
    
    def set_light_demo(self):
        l = 0
        while l <= 15:
            self.set_light(True, l, 255)
            sleep_ms(100)
            l +=1
        
        while l >= 0:
            self.set_light(True, l, 255)
            sleep_ms(100)
            l -=1
        
        self.set_light(True, 0, 0)

        l=0
        d=5
        while d <= 255:
            l=0
            while l <= 15:
                self.set_light(False, l, d)
                sleep_ms(50)
                l +=1
            d += 10
            if d > 100:
                d+= 40
        return

    def set_group(self):
        ...

"""




#10000000 Get/set config data
#10000001 Get group assignments

#01GRIIII Set LED values
#data byte LED duty cycle

group = False #(G)
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

"""