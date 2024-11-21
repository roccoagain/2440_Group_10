import math
import time
import machine
from machine import PWM, Pin, time_pulse_us
from ir_rx.nec import NEC_8

IR_MODE = True
PROTOCOL_TOGGLE_PIN = 9

# Protocol toggle pin
protocol_toggle = Pin(PROTOCOL_TOGGLE_PIN, Pin.IN, Pin.PULL_UP)


# Ultrasonic sensor pins
TRIG_PIN = 10
ECHO_PIN = 11
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Servo setup
SERVO_PIN = 15
servo_pwm = PWM(Pin(SERVO_PIN))
servo_pwm.freq(50)

# Motor pins
PWM_RATE = 2000
AIN1_PIN = 12
AIN2_PIN = 13
BIN1_PIN = 14
BIN2_PIN = 15

ain1_ph = Pin(AIN1_PIN, Pin.OUT)
ain2_en = PWM(Pin(AIN2_PIN))
ain2_en.freq(PWM_RATE)

bin1_ph = Pin(BIN1_PIN, Pin.OUT)
bin2_en = PWM(Pin(BIN2_PIN))
bin2_en.freq(PWM_RATE)

# IR receiver pin
IR_PIN = 16
ir_pin = Pin(IR_PIN, Pin.IN, Pin.PULL_UP)

# IR commands
CMD_UP = 0x10
CMD_DOWN = 0x11
CMD_CENTER = 0x12
CMD_LEFT = 0x13
CMD_RIGHT = 0x14
CMD_A = 0x15
CMD_B = 0x16
CMD_X = 0x17
CMD_Y = 0x18

# RF Pins
RF_D0 = 18
RF_D1 = 19
RF_D2 = 20
RF_D3 = 21

# setup rf pins
rf_pins = [
    Pin(RF_D0, Pin.IN, Pin.PULL_UP),
    Pin(RF_D1, Pin.IN, Pin.PULL_UP),
    Pin(RF_D2, Pin.IN, Pin.PULL_UP),
    Pin(RF_D3, Pin.IN, Pin.PULL_UP),
]


def measure_distance():
    """Measure distance using the ultrasonic sensor."""
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    duration = time_pulse_us(echo, 1, 30000)  # Timeout set to 30ms

    if duration < 0:
        return None  # Timeout occurred, no echo received

    distance = (duration * 0.0343) / 2  # Calculate distance in cm
    return distance


def spin():
    """Spin in a circle until the Ultrasonic sensor detects an obstacle."""
    motor_control(1, 50000, 0, 50000)
    while True:
        distance = measure_distance()
        if distance is not None and distance < 10:
            motor_control(0, 0, 0, 0)
            break


def set_servo_angle(angle):
    """Set servo to the specified angle (0-270 degrees)."""
    duty = int(2048 + (angle / 270) * 2048)
    servo_pwm.duty_u16(duty)


def motor_control(ain1, ain2_duty, bin1, bin2_duty):
    """Control motor direction and speed."""
    ain1_ph.value(ain1)
    ain2_en.duty_u16(ain2_duty)
    bin1_ph.value(not bin1)
    bin2_en.duty_u16(bin2_duty)


def ir_callback(data, addr, _):
    """Handle IR commands."""
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    if IR_MODE:
        # Forward
        if data == CMD_UP:
            print("Moving forward")
            motor_control(1, 50000, 1, 50000)

        # Reverse
        elif data == CMD_DOWN:
            print("Moving reverse")
            motor_control(0, 50000, 0, 50000)

        # Stop
        elif data == CMD_CENTER:
            print("Stopping motors")
            motor_control(0, 0, 0, 0)

        # Left
        elif data == CMD_LEFT:
            print("Turning left")
            motor_control(0, 25000, 1, 50000)

        # Right
        elif data == CMD_RIGHT:
            print("Turning right")
            motor_control(1, 50000, 0, 25000)

        # Lift servo
        elif data == CMD_A:
            print("Lifting servo")
            set_servo_angle(270)

        # Lower servo
        elif data == CMD_B:
            print("Lowering servo")
            set_servo_angle(0)

        # Spin in a circle
        elif data == CMD_X:
            spin()

        # Measure distance
        else:
            print(f"Unknown command: 0x{data:02X}")
            motor_control(0, 0, 0, 0)


# Initialize IR receiver
ir_receiver = NEC_8(ir_pin, callback=ir_callback)


# Main loop
def main():
    global IR_MODE
    print("System initialized. Waiting for IR commands...")
    while True:
        # If protocol toggle pin is high, switch to RF mode
        if protocol_toggle.value() == 1 and IR_MODE == True:
            print("Switching to RF mode")
            IR_MODE = False
            time.sleep(0.1)
        elif protocol_toggle.value() == 0 and IR_MODE == False:
            print("Switching to IR mode")
            IR_MODE = True
            time.sleep(0.1)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
