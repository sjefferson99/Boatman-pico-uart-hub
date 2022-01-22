import utime
import machine
from machine import Timer
import signalk
import uart

#TODO detect display and enable if present
enable_display = False

if enable_display:
    import picodisplay
    
    # Initialise Picodisplay with a bytearray display buffer
    print("initialising display, LED and buttons")
    buf = bytearray(picodisplay.get_width() * picodisplay.get_height() * 2)
    picodisplay.init(buf)
    picodisplay.set_backlight(1.0)

    picodisplay.set_pen(0, 255, 0)                      # Set a green pen
    picodisplay.clear()                                 # Clear the display buffer
    picodisplay.set_pen(255, 255, 255)                  # Set a white pen
    picodisplay.text("BoatMan", 10, 10, 240, 4)         # Add some text
    picodisplay.text("Boat Manager", 10, 50, 240, 2)    # Add some text
    picodisplay.update()                                # Update the display with our changes

    BUTTON_A = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
    BUTTON_B = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
    BUTTON_X = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
    BUTTON_Y = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

    #TODO - init display LED

    #Button debounce and config
    print("initialising button config variables")
    int_sample_freq = 10                            #Button debounce integrator sample frequenccy
    debounce_time = 0.1                             #seconds to debounce for
    int_max = int(int_sample_freq * debounce_time)  #integrator max value for button is pressed

    button_integrators = {"BUTTON_A" : 0, "BUTTON_B" : 0, "BUTTON_X" : 0, "BUTTON_Y" : 0}   #button debounce integrator values
    button_int_state = {"BUTTON_A" : 0, "BUTTON_B" : 0, "BUTTON_X" : 0, "BUTTON_Y" : 0}     #button integrator output last state
    button_times = {"BUTTON_A" : 0, "BUTTON_B" : 0, "BUTTON_X" : 0, "BUTTON_Y" : 0}         #button press time
    button_short = {"BUTTON_A" : 0, "BUTTON_B" : 0, "BUTTON_X" : 0, "BUTTON_Y" : 0}         #dictionary lookup of short pressed detection on buttons
    button_long = {"BUTTON_A" : 0, "BUTTON_B" : 0, "BUTTON_X" : 0, "BUTTON_Y" : 0}          #dictionary lookup of long pressed detection on buttons

    longpresstime = 1000    #button long press time in milliseconds

    lastactivity = 0        #activity timer on button presses
    modetimeout = 4000      #timeout to drop to run mode in ms

    #Button functions
    print("initialising button functions")
    #timer handler uses an integrator to debounce button presses and assign short or long press values based on time comparisons
    def button_debounce(timer):
        global button_integrators
        global button_long
        global button_short
        global button_times
        global lastactivity

        for button in button_integrators:

            if picodisplay.is_pressed(getattr(picodisplay, button)):    #Integrate button pressed this sample
                if button_integrators[button] < int_max:
                    button_integrators[button] += 1
            
            if picodisplay.is_pressed(getattr(picodisplay, button)) == False: #Integrate button not pressed this sample
                if button_integrators[button] > 0:
                    button_integrators[button] -= 1
        
            if button_integrators[button] == 0:         #integrator hit button value of 0
                #print("Button low: " + button)
                if button_int_state[button] == 1:       #on transition to 0 from 1
                    button_short[button] = 1
                    lastactivity = button_times[button] = utime.ticks_ms()
                    print("Short " + button)
                button_int_state[button] = 0
                
            if button_integrators[button] >= int_max:   #integrator hit button value of 1
                button_integrators[button] = int_max    #reset integrator in case corrupted
                if button_int_state[button] == 0:
                    button_times[button] = utime.ticks_ms()     #set transition high time if previous state was low
                if utime.ticks_diff(utime.ticks_ms(), button_times[button]) > longpresstime and button_int_state[button] == 1:    #set long press if it's been long enough and not already set long press
                    button_long[button] = 1
                    lastactivity = button_times[button] = utime.ticks_ms()
                    print("Long " + button)
                    button_int_state[button] = 2    #set int_state higher than 1 and don't reset if higher to avoid a short press triggering after the button is released on long press
                if button_int_state[button] < 2:
                    button_int_state[button] = 1

    #int_sample_freq seconds timer for button states
    print("initialising timer for button functions")
    tim = Timer()
    tim.init(freq=int_sample_freq, mode=Timer.PERIODIC, callback=button_debounce)

#Init onboard LED
print("initialising LED")
led = machine.Pin(25, machine.Pin.OUT)

#init I2C
print("initialising IO")
#TODO I2C init

#Init UART
print("initialising UART")
serial = uart.start_uart()

#TODO detect UART connection and set master hub if present
retries = 0 #init retries counter
maxretries = 3 #retry count
is_master_hub = True # override
#is_master_hub = False #For when detection is working

# while retries <= maxretries:
#     poll_uart() #clear buffer
#     uartdata = "Ping"
#     uart_send(uart, uartdata)
#     sleep(1) #Allow Pi server to repsond
#     uartdata = poll_uart()

#     if uartdata == "Boatman-PiZero":
#         is_master_hub = True
        
#     else:
#         retries +=1
#         if retries <= maxretries:
#             print("No server detected on UART, retrying")
#         else:
#             print("No Pi server found on UART, configuring as target on I2C bus")

print("is_master_hub: {}".format(is_master_hub))

#Configure I2C bus
sda=machine.Pin(16)
scl=machine.Pin(17)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)

#Scan I2C bus
print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))

#General variables
print("initialising general config")
refresh = 1     #screen refresh needed
current_mode = 0
modes = ["run", "lights", "misc"]
config_items = {"pir" : True, "option_2" : False}     #0=manual control; 1 = PIR control
config_item = 0 #misc config row select

#Main program loop
print("entering main program loop")

while True:
    
    jsondata = uart.poll_uart(serial)

    if jsondata:
        kdata = signalk.process_data(jsondata)
        print(signalk)
        ledvalue = kdata["light"]["1"]
        print(ledvalue)
        led.value(ledvalue)
    
    utime.sleep(1)

"""
    #TODO refactor to split light control from hub-display
    if enable_display:
        #Config time out
        if utime.ticks_diff(utime.ticks_ms(), lastactivity) > modetimeout and current_mode != 0:
            print("timing out config mode")
            current_mode = 0
            refresh = 1
        
        if current_mode == 0:   #run mode
            if refresh == 1:    #Update display
                print("refreshing display")
                picodisplay.set_pen(0, 255, 0)
                picodisplay.clear()                
                picodisplay.set_pen(255, 255, 255)       
                picodisplay.text("BoatMan", 10, 10, 240, 4)
                picodisplay.text("Boat Manager", 10, 40, 240, 2)
                picodisplay.text("X: Mode", 10, 70, 240, 2)
                picodisplay.update()
                refresh = 0

            if button_short["BUTTON_X"]:    #change mode
                current_mode = 1
                refresh = 1
                button_short["BUTTON_X"] = 0

        if current_mode == 1:   #In light config mode
            if button_short["BUTTON_A"]:    #toggle current led bank 0 or fader value
                ledbanks = toggleled(ledbanks)
                refresh = 1
                button_short["BUTTON_A"] = 0

            if button_short["BUTTON_B"]:    #increment current LED bank in cycle
                current_bank = changebank(current_bank)
                refresh = 1
                button_short["BUTTON_B"] = 0

            if button_long["BUTTON_B"]:    #Switch to global LED bank
                current_bank = 0
                refresh = 1
                button_long["BUTTON_B"] = 0

            if refresh == 1:    #Update display
                print("refreshing display")
                picodisplay.set_pen(0, 255, 0)
                picodisplay.clear()                
                picodisplay.set_pen(255, 255, 255)       
                picodisplay.text("BoatMan", 10, 10, 240, 4)
                picodisplay.text("Boat Manager", 10, 40, 240, 2)
                picodisplay.text("Light Config - Bank: " + str(current_bank), 10, 70, 240, 2)
                picodisplay.text("X: Mode", 10, 100, 240, 2)
                picodisplay.update()
                refresh = 0

            #Apply fader value only if bank is on
            if ledbanks[current_bank] > 0:
                    ledbanks[current_bank] = fader.read_u16()
            
            #Update LED duty cycles for global or individual modes
            # Need to design a passthrough so off/fade/on mode is selected by button a and remains as in when cycling through to misc config
            if current_bank == 0:
                ext_led1.duty_u16(ledbanks[0])
                ext_led2.duty_u16(ledbanks[0])
                ext_led3.duty_u16(ledbanks[0])
                ext_led4.duty_u16(ledbanks[0])
                ext_led5.duty_u16(ledbanks[0])
                ext_led6.duty_u16(0)
                ext_led7.duty_u16(0)
            else:
                ext_led1.duty_u16(ledbanks[1])
                ext_led2.duty_u16(ledbanks[2])
                ext_led3.duty_u16(ledbanks[3])
                ext_led4.duty_u16(ledbanks[4])
                ext_led5.duty_u16(ledbanks[5])
                ext_led6.duty_u16(ledbanks[6])
                ext_led7.duty_u16(ledbanks[7])

            if button_short["BUTTON_X"]:    #change mode
                current_mode = 2
                refresh = 1
                button_short["BUTTON_X"] = 0
        
        if current_mode == 2:    #enter misc config mode
            if refresh == 1:    #update display
                print("refreshing display")
                picodisplay.set_pen(0, 255, 0)
                picodisplay.clear()                
                picodisplay.set_pen(255, 255, 255)       
                picodisplay.text("Misc Config" , 10, 10, 240, 2)
                picodisplay.text("PIR Mode: " + str(config_items["pir"]), 10, 30, 240, 2)
                picodisplay.text("Option 2: " + str(config_items["option_2"]), 10, 50, 240, 2)
                #Need to move a selection rectangle over selected choice
                picodisplay.update()
                refresh = 0
            
            if button_short["BUTTON_B"]:
                print("changing config item")
                if config_item < (len(config_items) - 1):
                    config_item += 1
                else:
                    config_item = 0
                print(config_item)
                button_short["BUTTON_B"] = 0
                refresh = 1

            if button_short["BUTTON_A"]:
                config_items[list(config_items)[config_item]] = not config_items[list(config_items)[config_item]]
                button_short["BUTTON_A"] = 0
                refresh = 1
            
            if button_short["BUTTON_X"]:    #change mode
                current_mode = 0
                refresh = 1
                button_short["BUTTON_X"] = 0
                """