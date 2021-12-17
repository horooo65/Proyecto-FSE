# !/usr/bin/env python3
# ## ###############################################
#
# Autores: 
# Acosta Hernández Horacio Emmanuel
# Juárez Munguía Brandon Jesús
# Medina Cruz Josué Emanuel
# License: MIT
#
# ## ###############################################
#
# blink.py
# Control del encendido de leds
#
## ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import Raspberry Pi's GPIO control library
import RPi.GPIO as GPIO
# Imports sleep functon
from time import sleep
# Initializes virtual board (comment out for hardware deploy)
import virtualboard

# Disable warnings
# GPIO.setwarnings(False)
# Set up Rpi.GPIO library to use physical pin numbers
GPIO.setmode(GPIO.BOARD)

LEDS = [10, 12, 16, 18, 22, 24, 26, 32]

# Set up pins as output and default it to low
for led in LEDS:
	GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)


def run_blink(num):
	# Blink the led
	GPIO.output(LEDS[num - 1], GPIO.HIGH) # Turn led on
	sleep(0.3)                 # Espera 500ms
	GPIO.output(LEDS[num - 1], GPIO.LOW)  # Turn led off