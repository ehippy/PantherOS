# Circuit Playground NeoPixel
# ls /dev/tty.*
# screen /dev/tty.usbmodem14201 15200

import time
import board
import neopixel
import digitalio
 
import array
import math
 
import audiobusio
import random

print("Welcome to PatherOS")

button = digitalio.DigitalInOut(board.BUTTON_A)
button.switch_to_input(pull=digitalio.Pull.DOWN)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

pixel_brightness = 0.3 # don't go too high, it will die.

pixelLoop = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=pixel_brightness, auto_write=False)

pixelStrips = [
    neopixel.NeoPixel(board.A1, 30, brightness=pixel_brightness, auto_write=False),
    neopixel.NeoPixel(board.A7, 30, brightness=pixel_brightness, auto_write=False)
]

for strip in pixelStrips:
    strip[0] = GREEN
    strip.show()


# choose which demos to play
# 1 means play, 0 means don't!
color_chase_demo = 1
flash_demo = 1
rainbow_demo = 1
rainbow_cycle_demo = 1
 
 
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
 
def color_chase(color, wait):
    for i in range(10):
        pixelLoop[i] = color
        time.sleep(wait)
        pixelLoop.show()
    time.sleep(0.5)
 
 
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixelLoop[i] = wheel(rc_index & 255)
        pixelLoop.show()
        time.sleep(wait)
 
 
def rainbow(wait):
    for j in range(255):
        for i in range(len(pixelLoop)):
            idx = int(i + j)
            pixelLoop[i] = wheel(idx & 255)
        pixelLoop.show()
        time.sleep(wait)



# MIC STUPH

def mean(values):
    return sum(values) / len(values)
 
 
def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
 
    return math.sqrt(sum_of_samples / len(values))
 
 
mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)


def stealth_mode():
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    # print("mic mag: ", magnitude)

    mic_top_end = 300.0
    
    for i in range(10):
        color = OFF
        if ((magnitude/mic_top_end) > (i/10)):
            color = PURPLE
        pixelLoop[i] = color

    for i in range(30):
        color = OFF
        if ((magnitude/mic_top_end) > (i/30)):
            color = PURPLE

        for strip in pixelStrips:
            strip[i] = color

    pixelLoop.show()
    for strip in pixelStrips:
        strip.show()


def battle_mode():

    heartbeat()
    pixelLoop.fill(PURPLE)
    pixelLoop.brightness = rage_amt
    pixelLoop.show()

    for strip in pixelStrips:
        for i in range(strip.n):
            if random.randrange(10) > 2:
                strip[i] = PURPLE
            else:
                strip[i] = OFF
        strip.show()


rage_amt = 0.0
rage_max = pixel_brightness
rage_step = 0.05
rage_dir = rage_step

def heartbeat():
    global rage_amt
    global rage_dir
    if rage_amt > rage_max or rage_amt < 0.0:
        rage_dir = -1 * rage_dir
    
    rage_amt += rage_dir
    print("Rage Amt", rage_amt)

def rage_mode():
    heartbeat()

    pixelLoop.fill(RED)
    pixelLoop.brightness = rage_amt
    pixelLoop.show()

    for strip in pixelStrips:
        strip.fill(RED)
        strip.brightness = rage_amt
        strip.show()

def rainbow_party():
    
    j = random.randrange(255)
    for i in range(10):
        rc_index = (i * 256 // 10) + j * 5
        pixelLoop[i] = wheel(rc_index & 255)
    pixelLoop.show()

    for i in range(30):
        rc_index = (i * 256 // 10) + j * 5
        pixelStrips[0][i] = wheel(rc_index & 255)
        pixelStrips[1][i] = wheel(rc_index & 255)
    pixelStrips[0].show()
    pixelStrips[1].show()



panther_mode = 1

while True:

    if button.value:
        panther_mode = panther_mode + 1
        print("CHANGING PANTHER MODE", panther_mode)

        pixelLoop.brightness = pixel_brightness
        for strip in pixelStrips:
            strip.brightness = pixel_brightness
            
        if panther_mode > 4:
            panther_mode = 1
        time.sleep(0.25)
    

    if panther_mode == 1:
        battle_mode()
        
    if panther_mode == 2:
        stealth_mode()

    if panther_mode == 3:
        rage_mode()

    if panther_mode == 4:
        rainbow_party()
    


