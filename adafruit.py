import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

from digitalio import DigitalInOut, Direction, Pull

# Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

class Display:
    def __init__(self):
        # Create the I2C interface
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the SSD1306 OLED class
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        self.width = self.disp.width
        self.height = self.disp.height

    def _clearDisplay(self):
        self.disp.fill(0)
        self.disp.show()

    def run(self, on_draw):
        width = self.disp.width
        height = self.disp.height
        image = Image.new("1", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        self._clearDisplay()

        while True:
            # Draw black background
            draw.rectangle((0, 0, width, height), outline=0, fill=0) 
            on_draw(draw)
            self.disp.image(image)
            self.disp.show()

class Input:
    def __init__(self):

        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT
        self.button_A.pull = Pull.UP

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT
        self.button_B.pull = Pull.UP

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT
        self.button_L.pull = Pull.UP

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT
        self.button_R.pull = Pull.UP

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT
        self.button_U.pull = Pull.UP

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT
        self.button_D.pull = Pull.UP

    def up(self):
        return not self.button_U.value

    def down(self):
        return not self.button_D.value

    def left(self):
        return not self.button_L.value

    def right(self):
        return not self.button_R.value

    def button_top(self):
        return not self.button_B.value

    def button_bot(self):
        return not self.button_A.value