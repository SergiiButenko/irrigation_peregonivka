#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "NotebookNet";
const char* password = "0660101327";

ESP8266WebServer server(80);

const int r1 = D7;
const int r2 = D5;
const int led = D4;

void handleRoot() {
  server.send(200, "text/plain", "hello from esp8266!");
}

void handleNotFound(){
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void blink_led_01(){
  digitalWrite(led, 0);
  delay(500);
  digitalWrite(led, 1);
}

void blink_led_10(){
  digitalWrite(led, 1);
  delay(500);
  digitalWrite(led, 0);
}

void send_status(){
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    server.send(200, "application/json", "{\"1\":" + String(r1_status) + ", \"2\":" + String(r2_status) + "}");
}

void setup(void){
  Serial.println("setup");
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(r1, 0);
  digitalWrite(r2, 0);
  digitalWrite(led, 0);
  
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("done");
  blink_led_01();

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    blink_led_10();
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  blink_led_01();

  server.on("/", handleRoot);

  server.on("/test", [](){
    server.send(200, "text/plain", "this works as well");
    blink_led_01();
  });

  server.on("/on", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 1);
    if (relay == "2")  digitalWrite(r2, 1);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    send_status();
    blink_led_01();
  });

  server.on("/off", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 0);
    if (relay == "2")  digitalWrite(r2, 0);
    send_status();
    blink_led_01();
  });

  server.on("/status", [](){
    send_status();
    blink_led_01();
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();
}

