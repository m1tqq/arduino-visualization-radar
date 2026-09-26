# Arduino Radar Visualization

A real-time radar visualization system built using **Arduino** and **Python**.

An **HC-SR04 ultrasonic sensor** mounted on a servo motor scans a 180° area and sends angle/distance measurements over a serial connection. A Python application processes the incoming data and visualizes the scan in real time using a polar radar-style display.

> This project was developed as part of a university robotics course.
>
> My contribution focused on the Python side of the system: **serial communication, sensor data processing, simulation, and real-time radar visualization**.

---

## Features

- 180° environment scanning using a servo motor
- Distance measurement using an HC-SR04 ultrasonic sensor
- Arduino-to-Python serial communication
- Real-time polar radar visualization
- Continuous visualization of detected objects
- Simulation mode for testing the visualization without connected hardware

---

## How It Works

The Arduino continuously rotates the ultrasonic sensor between **0° and 180°**.

For every angle, it measures the distance to the nearest detected object and sends the measurement over the serial connection in the following format:

```text
angle,distance
```

Example:

```text
90,42
```

The Python application reads these measurements, stores the latest distance for each angle, and updates a Matplotlib polar plot in real time.

---

## Hardware

- Arduino Uno
- HC-SR04 Ultrasonic Sensor
- Servo Motor
- USB Connection

---

## Software

- Arduino / C++
- Python 3
- NumPy
- Matplotlib
- PySerial

---

## Project Structure

```text
arduino_radar/
├── arduino_radar/
│   └── arduino_radar.ino    # Arduino sensor and servo control
├── radar_serial.py          # Serial communication and live visualization
└── radar_sim.py             # Visualization simulation without hardware
```

---

## Running the Project

### 1. Arduino

Connect the components to the Arduino and upload:

```text
arduino_radar/arduino_radar/arduino_radar.ino
```

The Arduino sends measurements over serial at **9600 baud**.

### 2. Python dependencies

Install the required packages:

```bash
pip install numpy matplotlib pyserial
```

### 3. Serial port

Update the serial port in `radar_serial.py` if necessary:

```python
PORT = "/dev/tty.usbmodem1201"
```

### 4. Run the live visualization

```bash
python arduino_radar/radar_serial.py
```

---

## Simulation

The visualization can also be tested without physical hardware using randomly generated radar measurements:

```bash
python arduino_radar/radar_sim.py
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

`Arduino` · `C++` · `Python` · `NumPy` · `Matplotlib` · `PySerial` · `Serial Communication`
