#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

uint8_t GPIO_Pin = D7;
volatile byte state = 0;

const char *host = "http://mozz.asuscomm.com:7542";

const char* ssid = "NotebookNet";
const char* password = "0660101327";


void setup() {
  Serial.begin(115200);
  Serial.println(millis());
  Serial.println("started");
  attachInterrupt(digitalPinToInterrupt(GPIO_Pin), IntCallback, RISING);

  Serial.begin(115200);
  WiFi.setAutoConnect (true);
  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("done");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
  }

  if (state == 1) {
    HTTPClient http;

    http.begin(host + String("/stop_filling"));
    int httpCode = http.GET();            //Send the request
    String payload = http.getString();    //Get the response payload

    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

    state = 0;
    delay(5000);
  }
}

void IntCallback() {
  if (digitalRead(GPIO_Pin) == HIGH) {
    state = 1;
  }
}
