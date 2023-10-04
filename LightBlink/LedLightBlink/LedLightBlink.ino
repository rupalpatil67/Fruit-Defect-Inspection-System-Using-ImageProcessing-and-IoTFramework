// Include required libraries
#include <ESP8266WiFi.h>

// Define pins for the red and green LEDs
const int RED_LED_PIN = 12;
const int GREEN_LED_PIN = 14;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
 
  // Initialize the red and green LEDs as output pins
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
}

void loop() {
  // Wait for user input from the serial monitor
  while (Serial.available() == 0) {
    // Do nothing
  }
 
  // Read the user input from the serial monitor
  String input = Serial.readString();
 
  // Determine whether the input is fresh or rotten
  if (input.indexOf("fresh") != -1) {
    // Input is fresh, blink the green LED
    digitalWrite(GREEN_LED_PIN, HIGH);
    delay(5000);
    digitalWrite(GREEN_LED_PIN, LOW);
  } else if (input.indexOf("rotten") != -1) {
    // Input is rotten, blink the red LED
    digitalWrite(RED_LED_PIN, HIGH);
    delay(5000);
    digitalWrite(RED_LED_PIN, LOW);
  } else {
    // Input is not recognized, do nothing
  }
}
