"""Live radar: reads "angle,distance" lines from the Arduino over serial and
plots them in real time.

    python radar_serial.py                 # find the Arduino automatically
    python radar_serial.py --port COM3     # or name the port explicitly
"""

from __future__ import annotations

import argparse
import sys
import time

import serial
from serial.tools import list_ports

from radar import RadarDisplay, parse_measurement

DEFAULT_PORT = "/dev/tty.usbmodem1201"
BAUD = 9600
REDRAW_INTERVAL = 0.05  # seconds between plot updates

# Words that identify an Arduino (or a common USB-serial clone) in port listings.
ARDUINO_HINTS = ("arduino", "usbmodem", "ttyacm", "ch340", "usb serial", "wchusbserial")


def find_arduino_port() -> str | None:
    """Returns the first serial port that looks like an Arduino, if any."""
    for port in list_ports.comports():
        text = " ".join(filter(None, [port.device, port.description, port.manufacturer])).lower()
        if any(hint in text for hint in ARDUINO_HINTS):
            return port.device
    return None


def available_ports() -> str:
    ports = [f"  {p.device}  ({p.description})" for p in list_ports.comports()]
    return "\n".join(ports) if ports else "  (none found)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Live radar visualization for the Arduino radar.")
    parser.add_argument("--port", help="serial port of the Arduino, e.g. COM3 or /dev/ttyACM0 "
                                       "(default: detected automatically)")
    parser.add_argument("--baud", type=int, default=BAUD, help=f"baud rate (default: {BAUD})")
    args = parser.parse_args()

    port = args.port or find_arduino_port() or DEFAULT_PORT

    try:
        connection = serial.Serial(port, args.baud, timeout=1)
    except serial.SerialException as error:
        print(f"Could not open serial port {port}: {error}", file=sys.stderr)
        print(f"Available ports:\n{available_ports()}", file=sys.stderr)
        print("Use --port to choose one.", file=sys.stderr)
        return 1

    print(f"Reading from {port} at {args.baud} baud. Close the window or press Ctrl+C to stop.")

    # Opening the port resets the Arduino; give it time to start sending.
    time.sleep(2)

    # Drop anything received so far and the next (possibly cut-off) line, so a
    # partial line such as "0,4" from "90,42" is never taken as a measurement.
    connection.reset_input_buffer()
    connection.readline()

    radar = RadarDisplay()
    last_draw = time.time()

    try:
        with connection:
            while radar.is_open():
                raw = connection.readline().decode("utf-8", errors="ignore")
                measurement = parse_measurement(raw)
                if measurement is not None:
                    radar.update(*measurement)

                if time.time() - last_draw > REDRAW_INTERVAL:
                    radar.redraw()
                    last_draw = time.time()
    except KeyboardInterrupt:
        pass
    except serial.SerialException as error:
        print(f"Serial connection lost: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
