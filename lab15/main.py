import math
import time
import machine
from machine import PWM, Pin

time.sleep(1)  # Wait for USB to become ready

pwm_rate = 2000

# Set up pins and PWM
ain1_ph = Pin(12, Pin.OUT)
ain2_en = PWM(Pin(13), freq=pwm_rate)

bin1_ph = Pin(14, Pin.OUT)
bin2_en = PWM(Pin(15), freq=pwm_rate)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)  # Set PWM duty cycle

while True:
    # Motor ON
    print("Motor ON")  # Print to REPL
    ain1_ph.low()
    ain2_en.duty_u16(pwm)
    bin1_ph.low()
    bin2_en.duty_u16(pwm)
    time.sleep(1)

    # Reverse direction
    ain1_ph.high()
    ain2_en.duty_u16(pwm)
    bin1_ph.high()
    bin2_en.duty_u16(pwm)
    print("waiting")
    time.sleep(1)

    # Uncomment the following lines to turn the motors off after each cycle
    # print("Motor OFF")
    # ain1_ph.low()
    # ain2_en.duty_u16(0)
    # bin1_ph.low()
    # bin2_en.duty_u16(0)
    # time.sleep(2)
