import machine
from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx import print_error 

# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

# Setup and initialize the IR receiver
ir_pin = Pin(13, Pin.IN, Pin.PULL_UP)  # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# Infinite loop to keep the program running
while True:
    pass
