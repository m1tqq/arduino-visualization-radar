// Arduino radar: sweeps an HC-SR04 ultrasonic sensor on a servo from 0° to 180°
// and back, and sends one "angle,distance" line over serial for every degree.
//
// Serial output (9600 baud), one line per measurement:
//   angle,distance      e.g. "90,42"
// angle is in degrees (0-180), distance in centimetres.
// A distance of 0 means no echo was received.

#include <Servo.h>

// Wiring
const int trigPin = 11;
const int echoPin = 12;
const int servoPin = 9;

// Time for the servo to reach the next degree before measuring, in milliseconds.
const int stepDelayMs = 20;

// Maximum time to wait for an echo, in microseconds. Without a timeout,
// pulseIn() waits up to 1 second when no pulse arrives, which stalls the
// sweep. 40 ms covers the full range of the HC-SR04 (about 4 m), including
// the ~38 ms pulse it sends when nothing is in range.
const unsigned long echoTimeoutUs = 40000UL;

Servo radarServo;

// Sends a trigger pulse and returns the length of the echo pulse in
// microseconds, or 0 if no echo arrived before the timeout.
long measureEchoDuration() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  return pulseIn(echoPin, HIGH, echoTimeoutUs);
}

// Points the sensor at the given angle, measures the distance and sends it.
void scanAt(int angle) {
  radarServo.write(angle);
  delay(stepDelayMs);

  long duration = measureEchoDuration();

  // Sound travels about 0.034 cm per microsecond; the pulse covers the
  // distance twice (there and back), hence the division by 2.
  int distance = duration * 0.034 / 2;

  Serial.print(angle);
  Serial.print(",");
  Serial.println(distance);
}

void setup() {
  Serial.begin(9600);

  radarServo.attach(servoPin);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Sweep from 0° to 180°, then back from 180° to 0°.
  for (int angle = 0; angle <= 180; angle++) {
    scanAt(angle);
  }
  for (int angle = 180; angle >= 0; angle--) {
    scanAt(angle);
  }
}
