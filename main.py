#Pico will need to be flashed with Pimoroni micropython for display support
#https://github.com/pimoroni/pimoroni-pico

from utime import sleep_ms
from machine import Pin, I2C
#import bmdisplay
from pico_lights import pico_light_controller
from bmserial import bmserial

#Deals with debug messages appropriately
def debug(message, verbosity = 0):
    #TODO Support UART output (unsure if toggle signalk/debug or put debug into signalk format)
    if debug_enable and verbosity <= debug_verbosity:
        print(message)

#Enables printing debug messages
global debug_enable
debug_enable = True

global debug_verbosity
debug_verbosity = 0 #0=basic debug messages, 1=most debug messages, 2=all debug messages. >0 adds 1 second sleep in program loop

#Enable pico display module
#https://shop.pimoroni.com/products/pico-display-pack
#TODO detect display and enable if present
display_enable = True

if display_enable:
    #TODO run detection and if fail set display_enable = False
    debug("Display enabled")
    
#Enable pico light controller module
pico_lights_enable = True
pico_lights_address = 0x41

#Config I2C
sda1 = Pin(2)
scl1 = Pin(3)
i2c1_freq = 100000

# Init I2C
debug("Init I2C")
i2c1 = I2C(1, sda=sda1, scl=scl1, freq=i2c1_freq)

# Init UART
serial = bmserial()

#Scan i2C bus for devices
debug('i2c1 devices found at')
devices = i2c1.scan()
if devices:
    for i in devices:
        debug(i)

if pico_lights_enable:
    debug("Pico light module enabled")
    lights = pico_light_controller(i2c1, pico_lights_address)
    debug(lights.I2C_address)
    
    if lights.check_bus():
        debug("Pico lights controller found on bus")

        lights_module_version = lights.get_version()
        debug("Lights version: {}".format(lights_module_version))
    
        if lights_module_version != lights.version:
            debug("Lights module version does not equal hub lights module version, disabling lights module, please upgrade hub and module to same version")
            pico_lights_enable = False
        else:
            debug("Lights hub version matches module version")
            #Load group config from lights module
            debug("Loading group config from lights module")
            lights.get_groups() #type: ignore

    else:
        debug("Pico lights controller not found on bus, disabling module")
        pico_lights_enable = False

else:
    debug("No I2C devices found")

while True:
    debug("Entering program loop", 2)

    #Poll serial for SignalK commands
    debug("Polling serial in", 2)
    serialdata = serial.poll_bmserial()
    if serialdata[0] != 0:
        debug(serialdata, 2)
        debug(serialdata[0], 2)
        debug(serialdata[1], 2)

        if serialdata[0] == 1:
            debug("Valid JSON received", 2)

            if "Light control" in serialdata[1]:
                if pico_lights_enable:
                    debug("Light control command received: {}".format(serialdata[1]["Light control"]))

                    command = serialdata[1]["Light control"]
                    returncode = serial.light_controls(lights, command) #type: ignore
                    debug(returncode)

                    #Send command value back on serial UART
                    serial.send_bmserial(str(serialdata[1]["Light control"]))

                else:
                    debug("Light command received but module disabled")
                    serial.send_bmserial("Light module disabled")

    #For each enabled module, do module loop activities
    if display_enable:
        debug("Display loop activities", 2)
    
    if pico_lights_enable:
        debug("Light controller loop activities", 2) #TODO TRY address to catch device bus disconnect as won't scan bus each loop
    
    if debug_verbosity > 0:
        sleep_ms(1000)