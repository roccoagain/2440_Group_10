from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(18))      # Set the pin for the PWM object

pwm.freq(60)            # Set the frequency of the PWM signal

while True:
    for duty in range(65025):
        pwm.duty_u16(duty)
        sleep(0.0001)
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)
        sleep(0.0001)
