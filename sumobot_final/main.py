import math
import time
from machine import PWM, Pin, time_pulse_us
from ir_rx.nec import NEC_8

# Constants
# full motor speed is 50000
FULL_SPEED = 30000
HALF_SPEED = 15000
PWM_RATE = 2000

# Ultrasonic Sensor Pins
TRIG_PIN = 10
ECHO_PIN = 11

# Servo Setup
SERVO_PIN = 16  # Changed to avoid conflict with BIN2_PIN
SERVO_FREQ = 50

# Motor Pins
AIN1_PIN = 12
AIN2_PIN = 13
BIN1_PIN = 14
BIN2_PIN = 15

# IR Receiver Pin
IR_PIN = 18

RF_PINS = [
    Pin(7, Pin.IN, Pin.PULL_UP),  # D0
    Pin(6, Pin.IN, Pin.PULL_UP),  # D1
    Pin(5, Pin.IN, Pin.PULL_UP),  # D2
    Pin(4, Pin.IN, Pin.PULL_UP),  # D3
]

# IR Commands
CMD_UP = 0x11
CMD_DOWN = 0x10
CMD_CENTER = 0x12
CMD_LEFT = 0x13
CMD_RIGHT = 0x14
CMD_A = 0x15
CMD_B = 0x16
CMD_X = 0x17
CMD_Y = 0x18
CMD_START = 0x19
CMD_SELECT = 0x1A

# Initialize Ultrasonic Sensor
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Initialize Servo
servo_pwm = PWM(Pin(SERVO_PIN))
servo_pwm.freq(SERVO_FREQ)

# Initialize Motors
ain1_ph = Pin(AIN1_PIN, Pin.OUT)
ain2_en = PWM(Pin(AIN2_PIN))
ain2_en.freq(PWM_RATE)

bin1_ph = Pin(BIN1_PIN, Pin.OUT)
bin2_en = PWM(Pin(BIN2_PIN))
bin2_en.freq(PWM_RATE)

# Initialize IR Receiver
ir_pin = Pin(IR_PIN, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=lambda data, addr, _: ir_callback(data, addr))


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
    print(f"Distance: {distance} cm")
    return distance


def spin():
    """Spin in a circle until the ultrasonic sensor detects an obstacle."""
    motor_control(True, FULL_SPEED, False, FULL_SPEED)
    while True:
        distance = measure_distance()
        if distance is not None and distance < 30:  # Stop spinning if obstacle detected
            motor_control(False, 0, False, 0)
            break


def set_servo_angle(angle):
    """Set servo to the specified angle (0-270 degrees)."""
    min_duty = 2048
    max_duty = 8192

    duty = int(min_duty + (angle / 270) * (max_duty - min_duty))
    servo_pwm.duty_u16(duty)


def motor_control(ain1, ain2_duty, bin1, bin2_duty):
    """Control motor direction and speed."""
    ain1_ph.value(not ain1)
    ain2_en.duty_u16(ain2_duty)
    bin1_ph.value(bin1)
    bin2_en.duty_u16(bin2_duty)


def ir_callback(data, addr):
    """Handle IR commands."""
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

    if data == CMD_UP:
        print("Moving forward")
        motor_control(True, FULL_SPEED, True, FULL_SPEED)
    elif data == CMD_DOWN:
        print("Moving reverse")
        motor_control(False, FULL_SPEED, False, FULL_SPEED)
    elif data == CMD_CENTER:
        print("Stopping motors")
        motor_control(False, 0, False, 0)
    elif data == CMD_LEFT:
        print("Turning left")
        motor_control(False, FULL_SPEED, True, FULL_SPEED)
    elif data == CMD_RIGHT:
        print("Turning right")
        motor_control(True, FULL_SPEED, False, FULL_SPEED)
    elif data == CMD_A:
        print("Lifting servo")
        set_servo_angle(80)
    elif data == CMD_B:
        print("Lowering servo")
        set_servo_angle(0)
    elif data == CMD_X:
        print("Spinning")
        spin()
    elif data == CMD_START or data == CMD_SELECT:
        print("Stopping motors")
        motor_control(False, 0, False, 0)
    else:
        print(f"Unknown command: 0x{data:02X}")
        motor_control(False, 0, False, 0)


def read_rf_data():
    """Read RF data from RF pins."""
    rf_data = 0
    for i, pin in enumerate(RF_PINS):
        rf_data |= pin.value() << i
    return rf_data


# main loop handles RF commands
def main():
    print("Starting main loop...")
    while True:
        rf_data = read_rf_data()
        # do nothing if we receive 0x00
        if rf_data == 0x00:
            continue
        if rf_data == 0x08:
            print("Received, 0x08, Moving forward")
            motor_control(True, FULL_SPEED, True, FULL_SPEED)
        elif rf_data == 0x04:
            print("Received, 0x04, Moving reverse")
            motor_control(False, FULL_SPEED, False, FULL_SPEED)
        elif rf_data == 0x02:
            print("Received, 0x02, Stopping motors")
            motor_control(False, 0, False, 0)
        # elif rf_data == 0x02:
        #     print("Turning left")
        #     motor_control(False, HALF_SPEED, True, FULL_SPEED)
        elif rf_data == 0x01:
            print("Received, 0x01, Turning right")
            motor_control(True, FULL_SPEED, False, HALF_SPEED)
        time.sleep(0.1)

    # # test ultrasonic
    # while True:
    #     #measure distance
    #     distance = measure_distance()
    #     print(distance, "cm")
    #     time.sleep(0.5)

    # test servo
    # while True:
    #     for angle in [0, 80]:
    #         print(f"Setting angle to {angle}")
    #         set_servo_angle(angle)
    #         time.sleep(1)


if __name__ == "__main__":
    main()
