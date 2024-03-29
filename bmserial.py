from machine import UART
import json
from pico_lights import pico_light_controller

class bmserial:
    """
    Communication over serial UART for passing SignalK data to and from SignalK servers
    UART is on Pico UART 0 at 115200 baud as per Pico Hub spec.
    
    Module provides functions for sending, receiving and parsing data in SignalK JSON format over the serial UART.
    
    ***SignalK JSON structure TBC***
    """
    
    def __init__(self) -> None:
        self.interface = self.start_uart()

    def start_uart(self) -> UART:
        uart = UART(0, 115200)
        return uart

    def poll_bmserial(self) -> list:
        """
        Checks for data on the serial port and attempts to load it as a JSON stream
        Returns a list of two objects
        
        [returncode, data]
        returncode: 
            0: No data on serial interface
            1: Valid JSON loaded into data list item
            -1: Data was present on serial interface but was not valid JSON, data loaded into data list item 
        """
        serialdata = []
        serialdata.append(0)
        
        if self.interface.any():
            data = self.interface.read()
            try:
                serialdata.append(json.loads(data)) #type: ignore
                serialdata[0] = 1
            except:
                serialdata[0] = -1
                serialdata.append(data)

        return serialdata

    def send_bmserial(self, data: str) -> int:
        self.interface.write(data.encode('utf-8'))
        return 0