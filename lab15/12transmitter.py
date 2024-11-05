import machine
from machine import I2C, Pin, UART
import seesaw
import time

# Initialize I2C. Adjust pin numbers based on your Pico's configuration
i2c = I2C(0, scl=Pin(19), sda=Pin(18))

# Initialize UART for sending commands
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Arduino code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)

# Define button and joystick pin numbers as per the Arduino code
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15

# Button mask based on Arduino code
BUTTONS_MASK = (
    (1 << BUTTON_X)
    | (1 << BUTTON_Y)
    | (1 << BUTTON_A)
    | (1 << BUTTON_B)
    | (1 << BUTTON_SELECT)
    | (1 << BUTTON_START)
)

# Initialize last button states
last_buttons = 0

# Initialize joystick center position
joystick_center_x = 511
joystick_center_y = 497
joystick_threshold = 50  # Adjust threshold as needed


def setup_buttons():
    """Configure the pin modes for buttons."""
    seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)


def read_buttons():
    """Read and return the state of each button."""
    return seesaw_device.digital_read_bulk(BUTTONS_MASK)


def handle_button_press(button):
    """Send a command based on button press."""
    if button == BUTTON_A:
        uart.write("FORWARD\n")
        print("Sent command: FORWARD")
    elif button == BUTTON_B:
        uart.write("BACKWARD\n")
        print("Sent command: BACKWARD")
    elif button == BUTTON_X:
        uart.write("TURN_LEFT\n")
        print("Sent command: TURN_LEFT")
    elif button == BUTTON_Y:
        uart.write("TURN_RIGHT\n")
        print("Sent command: TURN_RIGHT")


def main():
    """Main program loop."""
    global last_buttons  # Ensure last_buttons is recognized as a global variable

    setup_buttons()

    last_x, last_y = seesaw_device.analog_read(
        JOYSTICK_X_PIN
    ), seesaw_device.analog_read(JOYSTICK_Y_PIN)

    while True:
        current_buttons = read_buttons()

        # Check if button state has changed
        for button in [BUTTON_A, BUTTON_B, BUTTON_X, BUTTON_Y]:
            if current_buttons & (1 << button) and not last_buttons & (1 << button):
                handle_button_press(button)

        # Read joystick values
        current_x = seesaw_device.analog_read(JOYSTICK_X_PIN)
        current_y = seesaw_device.analog_read(JOYSTICK_Y_PIN)

        # Check if joystick position has changed significantly
        if (
            abs(current_x - last_x) > joystick_threshold
            or abs(current_y - last_y) > joystick_threshold
        ):
            # Determine direction based on joystick position
            if current_y < joystick_center_y - joystick_threshold:
                uart.write("MOVE_UP\n")
                print("Sent command: MOVE_UP")
            elif current_y > joystick_center_y + joystick_threshold:
                uart.write("MOVE_DOWN\n")
                print("Sent command: MOVE_DOWN")
            elif current_x < joystick_center_x - joystick_threshold:
                uart.write("MOVE_LEFT\n")
                print("Sent command: MOVE_LEFT")
            elif current_x > joystick_center_x + joystick_threshold:
                uart.write("MOVE_RIGHT\n")
                print("Sent command: MOVE_RIGHT")

            last_x, last_y = current_x, current_y

        last_buttons = current_buttons
        time.sleep(0.1)  # Delay to prevent overwhelming the output


if __name__ == "__main__":
    main()
