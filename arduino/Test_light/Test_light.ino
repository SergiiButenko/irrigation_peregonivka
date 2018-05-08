#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "NotebookNet";
const char* password = "0660101327";
//const char* ssid = "faza_2";
//const char* password = "Kobe_2016";

uint8_t GPIO_Pin = D5;
volatile byte state = 0;


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
  // put your main code here, to run repeatedly:

}
