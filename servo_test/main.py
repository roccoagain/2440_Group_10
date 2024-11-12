from machine import Pin, PWM
from time import sleep

servo_pin = PWM(Pin(15))
servo_pin.freq(50)


def set_servo_angle(angle):
    duty = int(2048 + (angle / 270) * 2048)
    servo_pin.duty_u16(duty)


try:
    while True:
        for angle in range(0, 271, 10):
            set_servo_angle(angle)
            sleep(0.02)
        for angle in range(270, -1, -10):
            set_servo_angle(angle)
            sleep(0.02)

except KeyboardInterrupt:
    servo_pin.deinit()
