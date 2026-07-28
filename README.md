# Arduino Radar

A simple radar visualization system built with **Arduino** and **Python**.

The project uses an **HC-SR04 ultrasonic sensor** mounted on a **servo motor** to scan the surrounding area. Distance measurements are transmitted to a Python application over serial communication, where they are processed and displayed in real time as a radar-style visualization.

> Developed as a university project. I implemented the Python application responsible for serial communication, data processing, and real-time radar visualization.

---

## Features

- 180° environment scanning using a servo motor
- Distance measurement with the HC-SR04 ultrasonic sensor
- Serial communication between Arduino and Python
- Real-time radar visualization
- Live object detection display

---

## Hardware

- Arduino Uno
- HC-SR04 Ultrasonic Sensor
- Servo Motor
- USB Connection

---

## Software

- Python 3
- Matplotlib
- PySerial

---

## Project Structure

```
.
├── arduino_radar.ino
├── radar_serial.py
└── README.md
```

---

## Getting Started

1. Connect the Arduino board to your computer.
2. Upload `arduino_radar.ino` to the Arduino.
3. Update the serial port inside `radar_serial.py` if necessary.
4. Install the required Python packages:

```bash
pip install matplotlib pyserial
```

5. Run the application:

```bash
python radar_serial.py
```

---

## Demonstration

### Hardware Setup

https://drive.google.com/file/d/1MraulsgjDurmTQOjdV4mJprrjSNbUSZI/view?usp=sharing

### Demo Video 1

https://drive.google.com/file/d/14OXwk00mVM_XMqj0nrh-VkUtTGmzQbUU/view?usp=sharing

### Demo Video 2

https://drive.google.com/file/d/1sofLPVddKBKpiShZTT7O_SAnNK18dq66/view?usp=sharing

### Demo Video 3

https://drive.google.com/file/d/11c58CotUJq63cRjXeROMKPzh5b8_gLaZ/view?usp=sharing

---

## Technologies

- Arduino
- Python
- Matplotlib
- PySerial
- Serial Communication
