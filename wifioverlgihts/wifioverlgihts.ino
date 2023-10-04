#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "Raj";
const char* password = "12345678";
ESP8266WebServer server(80);

const int LED_GREEN = 14; // replace with the actual pin number for the green LED
const int LED_RED = 12; // replace with the actual pin number for the red LED

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  server.on("/message", [](){
    if (server.hasArg("message")) {
      String message = server.arg("message");
      Serial.println("Received message: " + message);
      if (message == "fresh") {
        digitalWrite(LED_GREEN, HIGH);
        delay(1000);
        digitalWrite(LED_GREEN, LOW);
      } else if (message == "rotten") {
        digitalWrite(LED_RED, HIGH);
        delay(1000);
        digitalWrite(LED_RED, LOW);
      }
    }
    server.send(200, "text/plain", "OK");
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
