import ir_tx
import time
import machine
from ir_tx.nec import NEC
from machine import Pin

tx_pin = Pin(17, Pin.OUT, value=0)
device_addr = 0x01

transmitter = NEC(tx_pin)

CMD_FORWARD = 0x10  # forward command
CMD_REVERSE = 0x11  # reverse command
CMD_STOP = 0x12  # stop command


def send_command(command):
    transmitter.transmit(device_addr, command)
    print(f"Command {hex(command)} transmitted.")


if __name__ == "__main__":
    while True:
        print("Sending Forward command...")
        send_command(CMD_FORWARD)
        time.sleep(3)

        print("Sending Stop command...")
        send_command(CMD_STOP)
        time.sleep(3)

        print("Sending Reverse command...")
        send_command(CMD_REVERSE)
        time.sleep(3)

        print("Sending Stop command...")
        send_command(CMD_STOP)
        time.sleep(3)
