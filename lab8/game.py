from machine import Pin
import time
import random


def callback1(pin):
    global interrupt_flag, debounce_time, button_pressed
    if time.ticks_ms() - debounce_time > 500:
        interrupt_flag = 1
        button_pressed = 1
        debounce_time = time.ticks_ms()


def callback2(pin):
    global interrupt_flag, debounce_time, button_pressed
    if time.ticks_ms() - debounce_time > 500:
        interrupt_flag = 1
        button_pressed = 2
        debounce_time = time.ticks_ms()


def callback3(pin):
    global interrupt_flag, debounce_time, button_pressed
    if time.ticks_ms() - debounce_time > 500:
        interrupt_flag = 1
        button_pressed = 3
        debounce_time = time.ticks_ms()


def callback4(pin):
    global interrupt_flag, debounce_time, button_pressed
    if time.ticks_ms() - debounce_time > 500:
        interrupt_flag = 1
        button_pressed = 4
        debounce_time = time.ticks_ms()


# flags for interrupts and debounce
interrupt_flag = 0
debounce_time = 0
button_pressed = 0

button1 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)
button3 = Pin(4, Pin.IN, Pin.PULL_UP)
button4 = Pin(5, Pin.IN, Pin.PULL_UP)
led1 = Pin(10, Pin.OUT)
led2 = Pin(11, Pin.OUT)
led3 = Pin(12, Pin.OUT)
led4 = Pin(13, Pin.OUT)

# interrupts for buttons
button1.irq(trigger=Pin.IRQ_FALLING, handler=callback1)
button2.irq(trigger=Pin.IRQ_FALLING, handler=callback2)
button3.irq(trigger=Pin.IRQ_FALLING, handler=callback3)
button4.irq(trigger=Pin.IRQ_FALLING, handler=callback4)

# level tracker
level = 1

# game loop
while True:
    if level == 5:
        print("You win!")
    else:
        print("Level: ", level)

    # generate a random sequence, length of sequence is equal to level
    game_sequence = []
    for n in range(level):
        game_sequence.append(random.randint(1, 4))

    # display the sequence to the player
    delay_time = 0.5
    for n in game_sequence:
        if n == 1:
            led1.on()
            time.sleep(delay_time)
            led1.off()
            time.sleep(delay_time)
        elif n == 2:
            led2.on()
            time.sleep(delay_time)
            led2.off()
            time.sleep(delay_time)
        elif n == 3:
            led3.on()
            time.sleep(delay_time)
            led3.off()
            time.sleep(delay_time)
        elif n == 4:
            led4.on()
            time.sleep(delay_time)
            led4.off()
            time.sleep(delay_time)

    # track the player's inputted sequence
    input_sequence = []

    # catch button presses
    while len(input_sequence) != len(game_sequence):
        if interrupt_flag is 1:
            input_sequence.append(button_pressed)
            interrupt_flag = 0

    # once the input sequence is long enough, check if it matches the game sequence
    if input_sequence == game_sequence:
        print("Correct")
        level += 1
    else:
        print("Incorrect")
        level = 1
    time.sleep(1)
