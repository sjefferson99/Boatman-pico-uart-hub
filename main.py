import machine

sda1 = machine.Pin(2)
scl1 = machine.Pin(3)
i2c1 = machine.I2C(1, sda=sda1, scl=scl1, freq=100000)

print('i2c1 devices found at')
devices = i2c1.scan()
if devices:
    for i in devices:
        print(i)


print("command register config")

#01GRIIII Set LED values
#data byte LED duty cycle

group = True #(G)
reset = True #(R)
id = 0 # (IIII)
duty = 0

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

senddata = bytearray(data)

i2c1.writeto(0x41, senddata)