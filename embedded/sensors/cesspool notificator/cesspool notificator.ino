#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPUpdateServer.h>
#include "common_lib.h"


/* setup function */
void setup(void) {
  for (byte i = 1; i < num_of_relay; i = i + 1) {
    pinMode(relay_pins[i], OUTPUT);
    digitalWrite(relay_pins[i], 0);
  }

  Serial.begin(115200);

  connect_to_wifi();
  send_notify();

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


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
  check_if_ping();
  check_if_notify();
  server.handleClient();
  MDNS.update();
  delay(1);
}
