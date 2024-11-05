# Blink 3 user LEDs using the pico.

from machine import Pin
from utime import sleep

# 3 led pins
pin1 = Pin(11, Pin.OUT)
pin2 = Pin(12, Pin.OUT)
pin3 = Pin(13, Pin.OUT)

print("LEDs start flashing...")
while True:
    try:
        pin1.toggle()
        pin2.toggle()
        pin3.toggle()
        sleep(1)
    except KeyboardInterrupt:
        break
pin1.off()
pin2.off()
pin3.off()
print("Finished.")