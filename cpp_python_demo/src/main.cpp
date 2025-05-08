#include <Arduino.h>

void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // Print a message to the Serial Monitor
  Serial.println("Hello from PlatformIO on Arduino Uno!");
}

void loop() {
  // Print a message to the Serial Monitor every second
  Serial.println("Looping...");
  delay(1000); // Wait for a second
} 