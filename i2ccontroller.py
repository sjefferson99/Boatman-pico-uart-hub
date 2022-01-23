from machine import Pin, I2C
from time import sleep

def format_hex(_object):
    """Format a value or list of values as 2 digit hex."""
    try:
        values_hex = [to_hex(value) for value in _object]
        return '[{}]'.format(', '.join(values_hex))
    except TypeError:
        # The object is a single value
        return to_hex(_object)

def to_hex(value):
    return '0x{:02X}'.format(value)

readbuffer=[0, 0]

i2c_controller = I2C(1,sda=Pin(2),scl=Pin(3),freq=100000)

print('Scanning I2C Bus for Responders...')
responder_addresses = i2c_controller.scan()
print('I2C Addresses of Responders found: ' + format_hex(responder_addresses))

buffer_out = bytearray([0x04, 0x08])
i2c_controller.writeto(0x41, buffer_out)

print("written I2C data {}".format(buffer_out))

sleep(2)

data = i2c_controller.readfrom(0x41, 2)

print("entering read loop")

for i, value in enumerate(data):
    readbuffer[i] = value

for datapoint in readbuffer:
    print(datapoint)