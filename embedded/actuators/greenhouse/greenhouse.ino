#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include "DHT.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include "common_lib.h"


#define DHTPIN D4     // what digital pin the DHT22 is conected to
#define ONE_WIRE_BUS 5
#define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature DS18B20(&oneWire);


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

/* setup function */
void setup(void) {
  for (byte i = 1; i < num_of_relay; i = i + 1) {
    pinMode(relay_pins[i], OUTPUT);
    digitalWrite(relay_pins[i], 0);
  }
  
  pinMode(DHTPIN, INPUT);
  dht.begin();

  Serial.begin(115200);
  
  connect_to_wifi();
  
  server.on("/status", send_status);
  server.on("/restart", restart_device);
  server.on("/test", test_system);
  server.on("/device_id", displayDeviceId);
  server.on("/on", turn_on);
  server.on("/off", turn_off);
  server.onNotFound(handleNotFound);

  server.on("/", HTTP_GET, []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/html", serverIndex);
  });

  server.on("/air_temperature", []() {
    delay(2000);
    float h = dht.readHumidity();
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();
    server.sendHeader("Connection", "close");
    server.send(200, "application/json", "{\"temp\":" + String(t) + ", \"hum\":" + String(h) + "}");
  });

  server.on("/ground_temperature", []() {
    delay(1000);
    float tempC = getTemperature();
    server.sendHeader("Connection", "close");
    server.send(200, "application/json", "{\"temp\":" + String(tempC) + "}");
  });

  server.on("/update", HTTP_POST, []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/plain", (Update.hasError()) ? "FAIL" : "OK");
    ESP.restart();
  }, []() {
    HTTPUpload& upload = server.upload();
    if (upload.status == UPLOAD_FILE_START) {
      Serial.setDebugOutput(true);
      WiFiUDP::stopAll();
      Serial.printf("Update: %s\n", upload.filename.c_str());
      uint32_t maxSketchSpace = (ESP.getFreeSketchSpace() - 0x1000) & 0xFFFFF000;
      if (!Update.begin(maxSketchSpace)) { //start with max available size
        Update.printError(Serial);
      }
    } else if (upload.status == UPLOAD_FILE_WRITE) {
      if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
        Update.printError(Serial);
      }
    } else if (upload.status == UPLOAD_FILE_END) {
      if (Update.end(true)) { //true to set the size to the current progress
        Serial.printf("Update Success: %u\nRebooting...\n", upload.totalSize);
      } else {
        Update.printError(Serial);
      }
      Serial.setDebugOutput(false);
    }
    yield();
  });

  server.begin();
}

void loop(void) {
  check_wifi_conn();
  server.handleClient();
  MDNS.update();
  delay(1);
}
