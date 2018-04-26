#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include "DHT.h"
#include <OneWire.h>
#include <DallasTemperature.h>

#define DHTPIN D4     // what digital pin the DHT22 is conected to
#define ONE_WIRE_BUS D1
#define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature DS18B20(&oneWire);

const char* ssid = "NotebookNet";
const char* password = "0660101327";

ESP8266WebServer server(80);

const int l1 = D5;
const int l2 = D6;
const int r1 = D7;
const int r2 = D8;


void blink_connected() {
  int l1_status = digitalRead(r1);
  int l2_status = digitalRead(r2);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  delay(100);
  digitalWrite(l1, 1);
  digitalWrite(l2, 1);
  delay(100);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  delay(100);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  delay(100);
  digitalWrite(l1, 1);
  digitalWrite(l2, 1);
  delay(100);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  delay(100);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  delay(100);
  digitalWrite(l1, 1);
  digitalWrite(l2, 1);
  delay(100);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  digitalWrite(l1, l1_status);
  digitalWrite(l2, l2_status);
}


void blink_led() {
  int l1_status = digitalRead(r1);
  int l2_status = digitalRead(r2);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);
  delay(200);
  digitalWrite(l1, 1);
  digitalWrite(l2, 1);
  delay(200);
  digitalWrite(l1, l1_status);
  digitalWrite(l2, l2_status);
}


void handleRoot() {
  server.send(200, "text/plain", "hello from esp8266!");
  blink_led();
}

void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  blink_led();
}

void setup(void) {
  Serial.println("setup");
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);

  digitalWrite(r1, 0);
  digitalWrite(r2, 0);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);

  Serial.begin(115200);
  WiFi.setAutoConnect (true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("done");
  blink_led();

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    blink_led();
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  blink_connected();

  server.on("/", handleRoot);

  server.on("/test", []() {
    server.send(200, "text/plain", "this works as well");
    blink_led();
  });

  server.on("/on", []() {
    String relay = server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 1);
    if (relay == "2")  digitalWrite(r2, 1);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    digitalWrite(l1, r1_status);
    digitalWrite(l2, r2_status);
    send_status();
    blink_led();
  });

  server.on("/off", []() {
    String relay = server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 0);
    if (relay == "2")  digitalWrite(r2, 0);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    send_status();
    digitalWrite(l1, r1_status);
    digitalWrite(l2, r2_status);
    blink_led();
  });

  server.on("/status", []() {
    send_status();
    blink_led();
  });

  server.on("/air_temperature", []() {
    delay(2000);
    float h = dht.readHumidity();
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();
    server.send(200, "application/json", "{\"temp\":" + String(t) + ", \"hum\":" + String(h) + "}");
    blink_led();
  });

  server.on("/ground_temperature", []() {
    delay(1000);
    float tempC = getTemperature();
    server.send(200, "application/json", "{\"temp\":" + String(tempC) + "}");
    blink_led();
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}

void send_status() {
  int r1_status = digitalRead(r1);
  int r2_status = digitalRead(r2);
  server.send(200, "application/json", "{\"1\":" + String(r1_status) + ", \"2\":" + String(r2_status) + "}");
}

float getTemperature() {
  float tempC = 0;
  int i = 2;
  for (int i=0; i<=30; i++){
    DS18B20.requestTemperatures(); 
    tempC = DS18B20.getTempCByIndex(0);
    if (tempC > (-127.0)){
      return tempC;
    }
    delay(100);
  }

  return tempC;
}
