"""
Picodisplay made by Pimoroni.
All information copied from 
https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/pico_display/README.md
as of 06/02/22
"""

def init(buffer: bytearray):
    """
    Sets up Pico Display. init must be called before any other functions since
    it configures the required PWM and GPIO. init() needs a bytearray type
    display buffer that MicroPython's garbage collection isn't going to eat,
    make sure you create one and pass it in like so:

    buf = bytearray(picodisplay.get_width() * picodisplay.get_height() * 2)
    picodisplay.init(buf)
    """
    ...

def set_backlight(brightness: float):
    """
    Sets the display backlight from 0.0 to 1.0.

    picodisplay.set_backlight(brightness)
    Uses hardware PWM to dim the display backlight, dimming values are
    gamma-corrected to provide smooth brightness transitions across the full
    range of intensity. This may result in some low values mapping as "off."
    """
    ...

def set_led(r: int, g: int, b: int):
    """
    Sets the RGB LED on Pico Display with an RGB triplet.

    picodisplay.set_led(r, g, b)
    Uses hardware PWM to drive the LED. Values are automatically
    gamma-corrected to provide smooth brightness transitions and low values may
    map as "off."
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

def update():
    """
    To display your changes on Pico Display's screen you need to call update.
    """
    ...

def set_pen(r_or_pen: int, g: int = 0, b: int = 0):
    """
    Sets the colour to be used by subsequent calls to drawing functions. The
    values for r, g and b should be from 0-255 inclusive.

    picodisplay.set_pen(r, g, b)

    Arguments g and b do not actually default to 0, but passing only one
    argument assumes a create_pen object, this allows pylance to accept one
    argument in this scenario.

    Can also accept a create_pen variable in place of r,g,b
    
    pen_colour = picodisplay.create_pen(r, g, b)
    picodisplay.set_pen(penColour)
    """
    ...

def create_pen(r: int, g: int, b: int) -> int:
    """
    Creates a pen which can be stored as a variable for faster re-use of the
    same colour through calls to set_pen. The values for r, g and b should be
    from 0-255 inclusive.

    pen_colour = picodisplay.create_pen(r, g, b)
    picodisplay.set_pen(penColour)
    """
    ...

def clear():
    """
    Fills the display buffer with the currently set pen colour.

    picodisplay.clear()
    """
    ...

def pixel(x: int, y: int):
    """
    Sets a single pixel in the display buffer to the current pen colour. The x
    and y parameters determine the X and Y coordinates of the drawn pixel in
    the buffer.

    picodisplay.pixel(x, y)
    """
    ...

def pixel_span(x: int, y: int, l: int):
    """
    Draws a horizontal line of pixels to the buffer. The x and y parameters
    specify the coordinates of the first pixel of the line. The l parameter
    describes the length of the line in pixels. This function will only extend
    the line towards the end of the screen, i.e. the x coordinate should
    specify the left hand extreme of the line.

    picodisplay.pixel_span(x, y, l)
    """
    ...

def rectangle(x: int, y: int, w: int, h: int):
    """
    Draws a rectangle filled with the current pen colour to the buffer. The x
    and y parameters specify the upper left corner of the rectangle, w
    specifies the width in pixels, and h the height.

    picodisplay.rectangle(x, y, w, h)
    
    https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/pico_display/images/rectangle.png
    """
    ...

def circle(x: int, y: int, r: int):
    """
    Draws a circle filled with the current pen colour to the buffer. The x and
    y parameters specify the centre of the circle, r specifies the radius in
    pixels.

    picodisplay.circle(x, y, r)

    https://github.com/pimoroni/pimoroni-pico/raw/main/micropython/modules/pico_display/images/circle.png
    """
    ...

def character(char_a: int, x: int, y: int, scale: int = 2):
    """
    Draws a single character to the display buffer in the current pen colour.
    The c parameter should be the ASCII numerical representation of the
    character to be printed, x and y describe the top-left corner of the
    character's drawing field. The character function can also be given an
    optional 4th parameter, scale, describing the scale of the character to be
    drawn. Default value is 2.

    char_a = ord('a')
    picodisplay.character(char_a, x, y)
    picodisplay.character(char_a, x, y, scale)
    """
    ...

def text(Text: str, x_offset: int, y_offset: int, wrap: int, scale: int = 2):
    """
    Draws a string of text to the display buffer in the current pen colour.
    The string parameter is the string of text to be drawn, and x and y specify
    the upper left corner of the drawing field. The wrap parameter describes
    the width, in pixels, after which the next word in the string will be drawn
    on a new line underneath the current text. This will wrap the string over
    multiple lines if required. This function also has an optional parameter,
    scale, which describes the size of the characters to be drawn. The default
    scale is 2.

    picodisplay.text(string, x, y, wrap)
    picodisplay.text(string, x, y, wrap, scale)

    https://github.com/pimoroni/pimoroni-pico/raw/main/micropython/modules/pico_display/images/text_scale.png
    """
    ...

def set_clip(x: int, y: int, w: int, h: int):
    """
    This function defines a rectangular area outside which no drawing actions
    will take effect. If a drawing action crosses the boundary of the clip then
    only the pixels inside the clip will be drawn. Note that clip does not
    remove pixels which have already been drawn, it only prevents new pixels
    being drawn outside the described area. A more visual description of the
    function of clips can be found below. Only one clip can be active at a
    time, and defining a new clip replaces any previous clips. The x and y
    parameters describe the upper-left corner of the clip area, w and h
    describe the width and height in pixels.

    picodisplay.set_clip(x, y, w, h)

    https://github.com/pimoroni/pimoroni-pico/raw/main/micropython/modules/pico_display/images/clip.png
    """
    ...

def remove_clip():
    """
    This function removes any currently implemented clip.
    """
    ...

def get_width() -> int:
    """
    Get width of the display in pixels
    """
    ...

def get_height() -> int:
    """
    Get height of the display in pixels
    """
    ...