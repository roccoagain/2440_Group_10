# Test that the IR receiver is working

import machine
from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx import print_error
from utime import sleep


# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    pin1.toggle()
    pin2.toggle()
    pin3.toggle()
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
    sleep(0.5)
    pin1.toggle()
    pin2.toggle()
    pin3.toggle()


pin1 = Pin(9, Pin.OUT)
pin2 = Pin(8, Pin.OUT)
pin3 = Pin(7, Pin.OUT)

# Setup and initialize the IR receiver
ir_pin = Pin(11, Pin.IN, Pin.PULL_UP)  # Adjust the pin number based on your wiring

ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# Infinite loop to keep the program running
while True:
    pass
