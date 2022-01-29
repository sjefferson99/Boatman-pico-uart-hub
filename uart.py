from machine import UART
from time import sleep
import json

def start_uart():
    uart = UART(0, 115200)
    print(uart)
    return uart

def poll_uart(serial):
    jsondata = ""
    if serial.any():
        data = serial.read()
        jsondata = json.loads(data)
        print("Debug SignalK - {}".format(jsondata))

    return jsondata

def uart_send(serial, uartdata):
  serial.write(uartdata.encode('utf-8'))
  return 0