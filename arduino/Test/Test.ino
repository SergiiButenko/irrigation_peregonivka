#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266mDNS.h>

byte delay_between_requests = 1000;
byte delay_between_filled_requests = 5000;
int delay_for_counter_millis = 10;
byte retry_limit = 5;

byte TIME_LIMIT_MINUTES = 30;
unsigned long current_time = 0;

const char *host = "http://192.168.1.22:8000";

const char *device_id = "kids_house";


//const char* ssid = "NotebookNet";
//const char* password = "0660101327";
const char* ssid = "faza_2";
const char* password = "Kobe_2016";

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

void check_wifi_connection(){
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wait for connection");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      blink_led();
      delay(500);
      Serial.print(".");
    }

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    blink_connected();
  }
}

void handleRoot() {
  server.send(200, "application/json", "{\"device_id\": \"" + String(device_id) +"\"");
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
  blink_led();
}


void send_status(){
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    server.send(200, "application/json", "{\"1\":" + String(r1_status) + ", \"2\":" + String(r2_status) + "}");
}

void send_request(String req){
  for (int i = 1; i <= retry_limit; i++) {
    HTTPClient http;

    Serial.println("Sending GET request:");
    Serial.println(req);
    Serial.print(i);
    Serial.print(" try out of ");
    Serial.print(retry_limit);
    Serial.print(". host:");
    Serial.println(host);

    http.begin(req);
    
    int httpCode = http.GET();            //Send the request
    String payload = http.getString();    //Get the response payload

    Serial.print("httpCode: ");
    Serial.println(httpCode);   //Print HTTP return code
    Serial.print("payload: ");
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

    if (httpCode == 200) {
      break;
    }

    delay(delay_between_requests);
  }
}


void ping() {
  if ( int((millis() - current_time) / 60000) >= TIME_LIMIT_MINUTES ) {
    send_ping();
    current_time = millis();
  }
}

void send_ping() {
  send_request(host + String("/im_alive?device_id=") + String(device_id));
}



void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  
  check_wifi_connection();
  // Port defaults to 8266
  // ArduinoOTA.setPort(8266);

  ArduinoOTA.setHostname(device_id);

  // No authentication by default
  // ArduinoOTA.setPassword("admin");

  // Password can be set with it's md5 value as well
  // MD5(admin) = 21232f297a57a5a743894a0e4a801fc3
  // ArduinoOTA.setPasswordHash("21232f297a57a5a743894a0e4a801fc3");

  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH)
      type = "sketch";
    else // U_SPIFFS
      type = "filesystem";

    // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  ArduinoOTA.begin();
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);
 
  digitalWrite(r1, 0);
  digitalWrite(r2, 0);
  digitalWrite(l1, 0);
  digitalWrite(l2, 0);

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/test", [](){
    server.send(200, "text/plain", "this works as well");
    blink_led();
  });

  server.on("/on", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 1);
    if (relay == "2")  digitalWrite(r2, 1);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    digitalWrite(l1, r1_status);
    digitalWrite(l2, r2_status);
    send_status();
    blink_led();
  });

  server.on("/off", [](){
    String relay=server.arg("relay");
    if (relay == "1")  digitalWrite(r1, 0);
    if (relay == "2")  digitalWrite(r2, 0);
    int r1_status = digitalRead(r1);
    int r2_status = digitalRead(r2);
    digitalWrite(l1, r1_status);
    digitalWrite(l2, r2_status);
    send_status();
    blink_led();
  });

  server.on("/status", [](){
    send_status();
    blink_led();
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");

  send_ping();
}

void loop() {
  check_wifi_connection();
  ArduinoOTA.handle();
  ping();
  server.handleClient();
}
