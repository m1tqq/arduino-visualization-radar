#include <Servo.h>

Servo radarServo;

const int trigPin = 11;
const int echoPin = 12;
const int servoPin = 9;

void setup() {
  Serial.begin(9600);

  radarServo.attach(servoPin);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  for (int angle = 0; angle <= 180; angle++) {
    radarServo.write(angle);
    delay(20);

    long duration = measureDistance();
    int distance = duration * 0.034 / 2;

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }

  for (int angle = 180; angle >= 0; angle--) {
    radarServo.write(angle);
    delay(20);

    long duration = measureDistance();
    int distance = duration * 0.034 / 2;

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}

long measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  return pulseIn(echoPin, HIGH);
}
