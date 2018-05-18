#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "NotebookNet";
const char* password = "0660101327";
//const char* ssid = "faza_2";
//const char* password = "Kobe_2016";
int state;

uint8_t INPUT_Pin = D5;
uint8_t OUT_Pin = D6;

void setup() {
  Serial.begin(115200);
  Serial.println("Setup");
  
  pinMode(INPUT_Pin, INPUT_PULLUP);
  pinMode(OUT_Pin, OUTPUT);

  Serial.begin(115200);
  WiFi.setAutoConnect(true);
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
  
  state = digitalRead(GPIO_Pin);
}


void loop() {
  Serial.println(digitalRead(OUT_Pin));
  delay(1000);
  revert_pin();
}


void revert_pin(){
  if (digitalRead(INPUT_Pin) != state){
    state = digitalRead(INPUT_Pin);
    Serial.println("STATE CHANGED");
    digitalWrite(OUT_Pin, !digitalRead(OUT_Pin));
  }
}




