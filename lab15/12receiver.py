import math, time
import machine
from machine import PWM, Pin
from ir_rx.nec import NEC_8


def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    if data == 0x10:  # Forward
        print("Moving motor forward")
        ain1_ph.value(1)
        ain2_en.duty_u16(50000)
        bin1_ph.value(1)
        bin2_en.duty_u16(50000)

    elif data == 0x11:  # Reverse
        print("Moving motor reverse")
        ain1_ph.value(0)
        ain2_en.duty_u16(50000)
        bin1_ph.value(0)
        bin2_en.duty_u16(50000)

    elif data == 0x12:  # Stop
        print("Stopping motor")
        ain2_en.duty_u16(0)
        bin2_en.duty_u16(0)

    elif data == 0x13:  # Turn Left
        print("Turning motor left")
        ain1_ph.value(0)
        ain2_en.duty_u16(25000)  # Reduce speed for turn
        bin1_ph.value(1)
        bin2_en.duty_u16(50000)

    elif data == 0x14:  # Turn Right
        print("Turning motor right")
        ain1_ph.value(1)
        ain2_en.duty_u16(50000)
        bin1_ph.value(0)
        bin2_en.duty_u16(25000)  # Reduce speed for turn


time.sleep(1)

pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT)
ain2_en = PWM(Pin(13), freq=pwm_rate, duty_u16=0)

bin1_ph = Pin(14, Pin.OUT)
bin2_en = PWM(Pin(15), freq=pwm_rate, duty_u16=0)

ir_pin = Pin(11, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)

while True:
    time.sleep(0.1)
