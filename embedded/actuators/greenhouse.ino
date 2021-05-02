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
  
  // connect to wifi

  blink_led();

  server.on("/", handleRoot);

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
    server.sendHeader("Connection", "close");
    server.send(200, "application/json", "{\"temp\":" + String(t) + ", \"hum\":" + String(h) + "}");
    blink_led();
  });

  server.on("/ground_temperature", []() {
    delay(1000);
    float tempC = getTemperature();
    server.sendHeader("Connection", "close");
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


// ==================== shared code ==========================
void startMDNS()
{
  /*use mdns for device_id name resolution*/
  if (!MDNS.begin(device_id, WiFi.localIP()))
  {
    Serial.println("Error setting up MDNS responder!");
    return;
  }

  Serial.println("mDNS responder started");
  MDNS.addService("http", "tcp", 80);
  Serial.printf("Ready! Open http://%s.local in your browser\n", device_id);
}

bool send_request(String req)
{
  int retry_limit = 5;
  int delay_between_requests = 1000;

  for (int i = 1; i <= retry_limit; i++)
  {
    HTTPClient http;

    Serial.println("Sending GET request:");
    Serial.println(req);
    Serial.print(i);
    Serial.print(" try out of ");
    Serial.print(retry_limit);
    Serial.print(". host:");
    Serial.println(host);

    http.begin(req);
    http.addHeader("X-Real-IP", WiFi.localIP().toString());

    int httpCode = http.GET();         //Send the request
    String payload = http.getString(); //Get the response payload

    Serial.print("httpCode: ");
    Serial.println(httpCode); //Print HTTP return code
    Serial.print("payload: ");
    Serial.println(payload); //Print request response payload

    http.end(); //Close connection

    if (httpCode == 200)
    {
      return true;
    }

    delay(delay_between_requests);
  }

  return false;
}

bool send_ping()
{
  return send_request(host + String("/im_alive?device_id=") + String(device_id));
}


bool set_expected_line_state()
{
  String req = host + String("/api/v1/devices/" + String(device_id) + String("/"));

  int retry_limit = 5;
  int delay_between_requests = 1000;

  for (int i = 1; i <= retry_limit; i++)
  {
    HTTPClient http;

    Serial.println("Sending GET request:");
    Serial.println(req);
    Serial.print(i);
    Serial.print(" try out of ");
    Serial.print(retry_limit);
    Serial.print(". host:");
    Serial.println(host);

    http.begin(req);
    http.addHeader("X-Real-IP", WiFi.localIP().toString());

    int httpCode = http.GET();         //Send the request
    String payload = http.getString(); //Get the response payload

    Serial.print("httpCode: ");
    Serial.println(httpCode); //Print HTTP return code
    Serial.print("payload: ");
    Serial.println(payload); //Print request response payload

    http.end(); //Close connection

    if (httpCode == 200)
    {
      DynamicJsonDocument doc(1024);
      DeserializationError error = deserializeJson(doc, payload);
      // Test if parsing succeeds.
      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return false;
      }

      // extract the values
      JsonArray array = doc["lines"].as<JsonArray>();
      for(JsonVariant v : array) {
        digitalWrite(relay_pins[v["relay_num"].as<int>()], v["expected_state"].as<int>());
        Serial.print("Relay: ");
        Serial.print(v["relay_num"].as<int>());
        Serial.print(" is set to: ");
        Serial.println(v["expected_state"].as<int>());
      }

      return true;
    }

    delay(delay_between_requests);
  }
}

void connect_to_wifi()
{
  WiFi.hostname(device_id);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  unsigned long previousMillis = millis();
  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    if (millis() - previousMillis >= 1000 * 60 * 5)
    {
      ESP.restart();
    }

    delay(1000);
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  while (send_ping() == false)
  {
    delay(1000 * 30);
  }

  startMDNS();
  set_expected_line_state();
}

void check_wifi_conn()
{
  if (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    Serial.println("Connecting to WIFI");
    connect_to_wifi();
  }
}

void displayDeviceId()
{
  String msg = "{";
  msg += "\"flash_version\":\"" + String(flash_version) + "\",";
  msg += "\"device_id\":\"" + String(device_id) + "\"";
  msg += "}";

  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
}

void restart_device()
{
  String msg = "{\"state\":\"restarted\"}";

  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
  ESP.restart();
}

void handleNotFound()
{
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++)
  {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.sendHeader("Connection", "close");
  server.send(404, "text/plain", message);
}


void check_if_ping()
{
  unsigned long current_time = 0;
  if (int((millis() - current_time) / 60000) >= 30)
  {
    send_ping();
    current_time = millis();
  }
}
