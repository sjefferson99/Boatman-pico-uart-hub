"""
Picodisplay made by Pimoroni
I've made this primarily to get rid of red squiggles in vscode pylance and is not associated with Pimoroni or in any way comprehensive.
What is defined should be accurate but not guarunteed.

Source:
https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/pico_display
"""

def get_width() -> int:
    """
    Get width
    """

def get_height() -> int:
    """
    Get height
    """
    ...

def init(buffer: bytearray):
    """
    Init buf
    """
    ...

def set_backlight(float):
    """
    Set backlight
    """
    ...

def set_pen(R, G, B):
    """
    Set pen colour
    """
    ...

def clear():
    """
    Clear display
    """
    ...

def text(Text: str, x_offset: int, y_offset: int, wrap: int, scale: int):
    """
    Draws a string of text to the display buffer in the current pen colour.
    The string parameter is the string of text to be drawn, and x and y specify
    the upper left corner of the drawing field. The wrap parameter describes
    the width, in pixels, after which the next word in the string will be drawn
    on a new line underneath the current text. This will wrap the string over
    multiple lines if required. This function also has an optional parameter,
    scale, which describes the size of the characters to be drawn. The default
    scale is 2.
    """
    ...

def update():
    """
    To display your changes on Pico Display's screen you need to call update.
    """
    ...

def is_pressed(button: int) -> bool:
    """
    Reads the GPIO pin connected to one of Pico Display's buttons, returning
    True if it's pressed and False if it is released.

    picodisplay.is_pressed(button)
    The button value should be a number denoting a pin, and constants
    picodisplay.BUTTON_A, picodisplay.BUTTON_B, picodisplay.BUTTON_X
    and picodisplay.BUTTON_Y are supplied to make it easier.

    is_a_button_pressed = picodisplay.is_pressed(picodisplay.BUTTON_A)
    """
    ...