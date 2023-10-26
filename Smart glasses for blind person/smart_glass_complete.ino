#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

#define UV_PIN A0
#define UV_THRESHOLD 200  // adjust this value to your specific sensor

SoftwareSerial mp3Serial(10, 11);  // RX, TX
DFRobotDFPlayerMini mp3;
const int trigPin = 3;
const int echoPin = 2;

long duration;
int distance;
int safetyDistance;

void setup() {
  Serial.begin(9600);
  mp3Serial.begin(9600);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  mp3.begin(mp3Serial);
  mp3.volume(30);  // set volume to 20 (max is 30)
}

void loop() {
  //int uvValue = analogRead(UV_PIN);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

// Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

// Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculating the distance
  distance= duration*0.034/2;
  if (distance < UV_THRESHOLD) {
    Serial.println("Object detected!");
    mp3.play(1);  // play audio file "0001.mp3" (make sure the file is in the root directory of your SD card)
    mp3.stop();
    delay(2000);  // wait for 4 seconds to avoid detecting the same object again
  }

  delay(100);  // wait for 100ms before checking the sensor again
}
