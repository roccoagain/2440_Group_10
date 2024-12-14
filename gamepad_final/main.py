import machine
from machine import I2C, Pin
import seesaw
from time import sleep
from ir_tx.nec import NEC

# Initialize I2C
I2C_SCL_PIN = 21
I2C_SDA_PIN = 20
I2C_ADDR = 0x50

i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))

# Initialize Seesaw device
seesaw_device = seesaw.Seesaw(i2c, addr=I2C_ADDR)

# Initialize IR transmitter
IR_TX_PIN = 17
DEVICE_ADDR = 0x01

tx_pin = Pin(IR_TX_PIN, Pin.OUT, value=0)
transmitter = NEC(tx_pin)

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
CMD_START = 0x19
CMD_SELECT = 0x1A

# Button and joystick configuration
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15

BUTTONS_MASK = (
    (1 << BUTTON_X)
    | (1 << BUTTON_Y)
    | (1 << BUTTON_A)
    | (1 << BUTTON_B)
    | (1 << BUTTON_SELECT)
    | (1 << BUTTON_START)
)

JOYSTICK_CENTER_X = 511
JOYSTICK_CENTER_Y = 497
JOYSTICK_THRESHOLD = 50

# Global variables for last states
last_buttons = 0
last_x, last_y = JOYSTICK_CENTER_X, JOYSTICK_CENTER_Y


def setup_buttons():
    """Configure the Seesaw pins for button input."""
    seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)


def read_buttons():
    """Read the current state of buttons."""
    return ~seesaw_device.digital_read_bulk(BUTTONS_MASK) & BUTTONS_MASK


def read_joystick():
    """Read the current position of the joystick."""
    x = seesaw_device.analog_read(JOYSTICK_X_PIN)
    y = seesaw_device.analog_read(JOYSTICK_Y_PIN)
    return x, y


def joystick_direction(x, y):
    """Determine joystick direction based on thresholds."""
    if y < JOYSTICK_CENTER_Y - JOYSTICK_THRESHOLD:
        return CMD_UP
    elif y > JOYSTICK_CENTER_Y + JOYSTICK_THRESHOLD:
        return CMD_DOWN
    elif x < JOYSTICK_CENTER_X - JOYSTICK_THRESHOLD:
        return CMD_LEFT
    elif x > JOYSTICK_CENTER_X + JOYSTICK_THRESHOLD:
        return CMD_RIGHT
    elif (
        abs(x - JOYSTICK_CENTER_X) <= JOYSTICK_THRESHOLD
        and abs(y - JOYSTICK_CENTER_Y) <= JOYSTICK_THRESHOLD
    ):
        return CMD_CENTER
    return None


def handle_button_press(buttons):
    """Handle button press events."""
    if buttons & (1 << BUTTON_A):
        send_command(CMD_A)
    elif buttons & (1 << BUTTON_B):
        send_command(CMD_B)
    elif buttons & (1 << BUTTON_X):
        send_command(CMD_X)
    elif buttons & (1 << BUTTON_Y):
        send_command(CMD_Y)


def send_command(command):
    """Send an IR command."""
    transmitter.transmit(DEVICE_ADDR, command)
    print(f"Command {hex(command)} transmitted.")


def main():
    """Main program loop."""
    global last_buttons, last_x, last_y

    setup_buttons()

    while True:
        # Read current button and joystick states
        current_buttons = read_buttons()
        current_x, current_y = read_joystick()

        # Handle joystick movement
        if (
            abs(current_x - last_x) > JOYSTICK_THRESHOLD
            or abs(current_y - last_y) > JOYSTICK_THRESHOLD
        ):
            command = joystick_direction(current_x, current_y)
            if command:
                send_command(command)
            last_x, last_y = current_x, current_y

        if current_buttons != last_buttons:
            handle_button_press(current_buttons)
            last_buttons = current_buttons

        sleep(0.1)  # Small delay to prevent overwhelming the system


if __name__ == "__main__":
    main()
