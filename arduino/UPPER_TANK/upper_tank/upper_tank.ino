#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

uint8_t GPIO_Pin = D6;
volatile byte state = 0;
volatile byte counter = 0;
uint8_t counter_max = 50;

const char *host = "http://mozz.asuscomm.com:7542";

const char* ssid = "NotebookNet";
const char* password = "0660101327";
//const char* ssid = "faza_2";
//const char* password = "Kobe_2016";



void setup() {
  Serial.begin(115200);
  Serial.println("Setup");
  
  pinMode(GPIO_Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(GPIO_Pin), IntCallback, RISING);

  Serial.begin(115200);
  WiFi.setAutoConnect (true);
  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  Serial.println("Finished");

  Serial.println("Wait for connection");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wait for connection");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  }

  if (state == 1) {
    Serial.println("Initialising http connection");
    HTTPClient http;
    
    Serial.print("Sending GET request");
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
  Serial.println("Interrupt signal received. Checking...");
  if (digitalRead(GPIO_Pin) == HIGH) {
    Serial.println("Signal is HIGH");
    counter++;
  } else {
    counter = 0;
  }

  if (counter >= counter_max) {
    state = 1;
    counter = 0;
  }
}
