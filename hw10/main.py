from machine import Pin
import time

debounce_time = 0


def callback1(pin):
    global debounce_time
    if time.ticks_ms() - debounce_time > 500:
        led1.on()
        debounce_time = time.ticks_ms()
        while True:
            pass


def callback2(pin):
    global debounce_time
    if time.ticks_ms() - debounce_time > 500:
        led2.on()
        debounce_time = time.ticks_ms()
        while True:
            pass


def callback3(pin):
    global debounce_time
    if time.ticks_ms() - debounce_time > 500:
        led3.on()
        debounce_time = time.ticks_ms()
        while True:
            pass


button1 = Pin(7, Pin.IN, Pin.PULL_UP)
button2 = Pin(8, Pin.IN, Pin.PULL_UP)
button3 = Pin(9, Pin.IN, Pin.PULL_UP)
led1 = Pin(10, Pin.OUT)
led2 = Pin(11, Pin.OUT)
led3 = Pin(12, Pin.OUT)

button1.irq(trigger=Pin.IRQ_FALLING, handler=callback1)
button2.irq(trigger=Pin.IRQ_FALLING, handler=callback2)
button3.irq(trigger=Pin.IRQ_FALLING, handler=callback3)

while True:
    time.sleep(0.1)
