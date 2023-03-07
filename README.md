# Archived project - This functionality is now being continued in https://github.com/sjefferson99/pico-boat-assistant

# Boatman hub with UART control and display v0.1

## Overview
The Boatman UART display hub module forms part of a wider Boatman ecosystem documented in the [Boatman project repository](https://github.com/sjefferson99/Boatman-project).

The hardware detailed below is built around the relatively new Raspberry Pi Pico microprocessor using the pimoroni customised micropython firmware option.

The module provides a small display with 4 button input for standalone operation and feedback as well as a serial UART connection intended to work with some form of web server or similar interface capable of sending and receiving appropriate JSON for Boatman control and feedback.

Child modules within the Boatman ecosystem connect via the I2C bus and the hub acts as an I2C master when communicating.

Other hub modules may be present and also act as I2C masters. At present, the child modules flag when configuration has been updated by a hub module and hubs will reconfigure based on more recent updates to bring themselves up to date via the child module rather than directly communicating.

### Compatible hub modules
- [Pico wireless hub](https://github.com/sjefferson99/Boatman-pico-wireless-hub)

### Compatible child modules
- [Pico lights module](https://github.com/sjefferson99/Boatman-pico-lights)

## Wiring pinout
The module uses an off the shelf Pico display pack from Pimoroni, which will tie up certain pins that will not be available for customisation. The pins in use should be determined by combining the two diagrams below for the display pack and the module specific pins.

### Pico display pinout
![Pico display pinout](/pico_display_pinout.png)

### Boatman display hub pinout
![Boatman display hub pinout](/Display%20PICO%20Pinout.drawio.png)

## Pico firmware
This module release was developed against the customised Pimoroni firmware [v1.18.4](https://github.com/pimoroni/pimoroni-pico/releases/download/v1.18.4/pimoroni-pico-v1.18.4-micropython.uf2)

More details can be found on the [release page](https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.18.4)

## Configuration
The hub module will identify when child module configuration is out of date and automatically pull this back on first run. No further configuration is required for the default setup.

## Hardware
- [Raspberry Pi Pico](https://thepihut.com/products/raspberry-pi-pico)
- [Pico Display Pack](https://thepihut.com/products/pico-display-pack)
