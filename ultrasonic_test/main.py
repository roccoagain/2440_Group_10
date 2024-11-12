from machine import Pin, PWM, time_pulse_us
import time

# -----------------------------------
# Configuration for Ultrasonic Sensor
# -----------------------------------
TRIG_PIN = 10
ECHO_PIN = 11

# -----------------------------------
# Configuration for Motor Control
# -----------------------------------
# Motor A
MOTOR_A_PH = 17  # Motor A Phase pin (Direction control)
MOTOR_A_EN = 19  # Motor A Enable pin (Speed control via PWM)

# Motor B
MOTOR_B_PH = 18  # Motor B Phase pin (Direction control)
MOTOR_B_EN = 20  # Motor B Enable pin (Speed control via PWM)

# -----------------------------------
# Initialize Ultrasonic Sensor Pins
# -----------------------------------
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# -----------------------------------
# Initialize Motor Control Pins
# -----------------------------------
# Phase Pins (Digital Outputs)
motor_a_ph = Pin(MOTOR_A_PH, Pin.OUT)
motor_b_ph = Pin(MOTOR_B_PH, Pin.OUT)

# Enable Pins (PWM Outputs)
motor_a_en = PWM(Pin(MOTOR_A_EN))
motor_b_en = PWM(Pin(MOTOR_B_EN))

# Set PWM Frequencies
pwm_rate = 1000  # Set PWM frequency to 1 kHz
motor_a_en.freq(pwm_rate)
motor_b_en.freq(pwm_rate)

# -----------------------------------
# Helper Functions
# -----------------------------------

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

def stop_motors():
    """Stop both motors by setting PWM duty cycles to 0."""
    motor_a_en.duty_u16(0)
    motor_b_en.duty_u16(0)

def move_forward():
    """Move both motors forward at 75% speed."""
    motor_a_ph.value(1)  # Forward direction
    motor_b_ph.value(1)
    motor_a_en.duty_u16(50000)  # 75% duty cycle
    motor_b_en.duty_u16(50000)  # 75% duty cycle

def move_tight_circle():
    """Move in a tight circle by adjusting motor speeds."""
    motor_a_ph.value(1)
    motor_b_ph.value(1)
    motor_a_en.duty_u16(50000)  # Motor A at 75%
    motor_b_en.duty_u16(25000)  # Motor B at 37.5% for tighter turn
    time.sleep(0.1)  # Duration of the maneuver

# -----------------------------------
# Main Loop
# -----------------------------------
try:
    while True:
        distance = measure_distance()

        if distance is not None:
            print(f"Distance: {distance:.2f} cm")
            if distance < 20:
                stop_motors()
                print("Motors stopped.")
            else:
                move_tight_circle()
                print("Moving in a tight circle.")
        else:
            print("No echo received. Unable to measure distance.")
            stop_motors()

        time.sleep(1)  # Delay before the next measurement

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    stop_motors()  # Ensure motors are stopped when exiting
