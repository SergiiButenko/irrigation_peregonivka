/*
   Copyright (c) 2015, Majenko Technologies
   All rights reserved.

   Redistribution and use in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

 * * Redistributions of source code must retain the above copyright notice, this
     list of conditions and the following disclaimer.

 * * Redistributions in binary form must reproduce the above copyright notice, this
     list of conditions and the following disclaimer in the documentation and/or
     other materials provided with the distribution.

 * * Neither the name of Majenko Technologies nor the names of its
     contributors may be used to endorse or promote products derived from
     this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
   ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "NotebookNet"
#define STAPSK  "0660101327"
#endif

const char *device_id = "irrigation1";
const char *ssid = STASSID;
const char *password = STAPSK;

ESP8266WebServer server(80);

const int r1 = D1;
const int r2 = D2;
const int r3 = D3;
const int r4 = D4;
const int r5 = D5;
const int r6 = D6;
const int r7 = D7;
const int r8 = D8;
const int led = 13;

void handleRoot() {
  server.send(200, "text/plain", device_id);
}

void handleNotFound() {
  digitalWrite(led, 1);
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
  digitalWrite(led, 0);
}

void send_status(){
    String msg = "{";
    msg += "\"1\":\"" + String(digitalRead(r1)) + "\",";
    msg += "\"2\":\"" + String(digitalRead(r2)) + "\",";
    msg += "\"3\":\"" + String(digitalRead(r3)) + "\",";
    msg += "\"4\":\"" + String(digitalRead(r4)) + "\",";
    msg += "\"5\":\"" + String(digitalRead(r5)) + "\",";
    msg += "\"6\":\"" + String(digitalRead(r6)) + "\",";
    msg += "\"7\":\"" + String(digitalRead(r7)) + "\",";
    msg += "\"8\":\"" + String(digitalRead(r8)) + "\"";
    msg += "}";
    
    Serial.println("Message to send:" + msg);
    server.send(200, "application/json", msg);
}

void setup(void) {
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);

  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r4, OUTPUT);
  pinMode(r5, OUTPUT);
  pinMode(r6, OUTPUT);
  pinMode(r7, OUTPUT);
  pinMode(r8, OUTPUT);
  
  digitalWrite(r1, 0);
  digitalWrite(r2, 0);
  digitalWrite(r3, 0);
  digitalWrite(r4, 0);
  digitalWrite(r5, 0);
  digitalWrite(r6, 0);
  digitalWrite(r7, 0);
  digitalWrite(r8, 0);

  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

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

  if (MDNS.begin(device_id)) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.on("/status", send_status);
  server.onNotFound(handleNotFound);

  server.on("/on", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 1);
    if (relay == "2")  digitalWrite(r2, 1);
    if (relay == "3")  digitalWrite(r3, 1);
    if (relay == "4")  digitalWrite(r4, 1);
    if (relay == "5")  digitalWrite(r5, 1);
    if (relay == "6")  digitalWrite(r6, 1);
    if (relay == "7")  digitalWrite(r7, 1);
    if (relay == "8")  digitalWrite(r8, 1);
    
    send_status();
  });

  server.on("/off", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 0);
    if (relay == "2")  digitalWrite(r2, 0);
    if (relay == "3")  digitalWrite(r3, 0);
    if (relay == "4")  digitalWrite(r4, 0);
    if (relay == "5")  digitalWrite(r5, 0);
    if (relay == "6")  digitalWrite(r6, 0);
    if (relay == "7")  digitalWrite(r7, 0);
    if (relay == "8")  digitalWrite(r8, 0);
    
    send_status();
  });
  
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
