import math
from types import SimpleNamespace

import pytest

import radar_serial
import radar_sim
from radar import MAX_ANGLE, RadarDisplay, parse_measurement


# ---- parsing serial lines ---------------------------------------------------

@pytest.mark.parametrize("line, expected", [
    ("90,42", (90, 42.0)),
    ("0,15\r\n", (0, 15.0)),
    ("180,0", (180, 0.0)),
    ("  45 , 7 ", (45, 7.0)),
])
def test_parses_valid_lines(line, expected):
    assert parse_measurement(line) == expected


@pytest.mark.parametrize("line", [
    "",            # timeout, nothing received
    "90",          # cut-off line
    "90,42,7",     # too many fields
    "abc,42",      # not a number
    "90,abc",
    "181,42",      # angle out of range
    "-1,42",
    "90,-5",       # negative distance
])
def test_rejects_invalid_lines(line):
    assert parse_measurement(line) is None


# ---- radar display ----------------------------------------------------------

def test_stores_latest_distance_per_angle():
    radar = RadarDisplay()
    radar.update(30, 100)
    radar.update(30, 80)
    assert radar.distances[30] == 80
    assert math.isnan(radar.distances[31])


def test_no_echo_leaves_a_gap_instead_of_a_point_at_the_centre():
    radar = RadarDisplay()
    radar.update(90, 0)
    assert math.isnan(radar.distances[90])


def test_redraw_plots_one_point_per_angle():
    radar = RadarDisplay()
    radar.update(10, 50)
    radar.redraw()
    assert len(radar.line.get_xdata()) == MAX_ANGLE + 1
    assert radar.is_open()


# ---- finding the Arduino ----------------------------------------------------

def fake_port(device, description="n/a", manufacturer=None):
    return SimpleNamespace(device=device, description=description, manufacturer=manufacturer)


def test_finds_arduino_port(monkeypatch):
    monkeypatch.setattr(radar_serial.list_ports, "comports", lambda: [
        fake_port("/dev/ttyS0"),
        fake_port("COM4", "Arduino Uno (COM4)", "Arduino LLC"),
    ])
    assert radar_serial.find_arduino_port() == "COM4"


def test_finds_clone_boards(monkeypatch):
    monkeypatch.setattr(radar_serial.list_ports, "comports", lambda: [
        fake_port("/dev/ttyUSB0", "USB2.0-Serial", "QinHeng Electronics CH340"),
    ])
    assert radar_serial.find_arduino_port() == "/dev/ttyUSB0"


def test_no_arduino_found(monkeypatch):
    monkeypatch.setattr(radar_serial.list_ports, "comports", lambda: [fake_port("/dev/ttyS0")])
    assert radar_serial.find_arduino_port() is None


# ---- simulation -------------------------------------------------------------

def test_simulated_room_is_within_plot_range():
    for angle in range(MAX_ANGLE + 1):
        assert 0 < radar_sim.room_distance(angle) <= 200


def test_simulated_room_shape():
    assert radar_sim.room_distance(0) == pytest.approx(radar_sim.ROOM_HALF_WIDTH)
    assert radar_sim.room_distance(90) == pytest.approx(radar_sim.ROOM_DEPTH)
    assert radar_sim.room_distance(140) == 45  # an object


def test_sweep_follows_the_servo():
    sweep = radar_sim.sweep_angles()
    angles = [next(sweep) for _ in range(2 * (MAX_ANGLE + 1) + 1)]
    assert angles[:3] == [0, 1, 2]
    assert angles[MAX_ANGLE] == MAX_ANGLE
    assert angles[MAX_ANGLE + 1] == MAX_ANGLE  # turns around, like the Arduino
    assert angles[-2:] == [0, 0]               # and starts the next sweep
