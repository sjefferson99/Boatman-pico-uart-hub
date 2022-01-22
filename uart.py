from machine import UART
from time import sleep
import json

def start_uart():
    uart = UART(0, 115200)
    print(uart)
    return uart

def poll_uart(uart):
    jsondata = ""
    if uart.any():
        data = uart.read()
        jsondata = json.loads(data)
        print("Debug SignalK - {}".format(jsondata))

    return jsondata

def uart_send(uart, uartdata):
  uart.write(uartdata.encode('utf-8'))
  return 0