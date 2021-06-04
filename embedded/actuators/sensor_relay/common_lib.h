#include "settings.h"
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

unsigned long previousMillis = 0;
unsigned long current_time = 0;
const long esp_restart_interval = 1000 * 60 * 5;

ESP8266WebServer server(80);
const char *serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";

void send_status()
{
  String msg = "{";
  for (byte i = 1; i < num_of_relay - 1; i = i + 1)
  {
    msg += "\"" + String(i) + "\":\"" + String(digitalRead(relay_pins[i])) + "\",";
  }
  msg += "\"" + String(num_of_relay - 1) + "\":\"" + String(digitalRead(relay_pins[num_of_relay - 1])) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
}

void turn_on()
{
  String relay = server.arg("relay");
  digitalWrite(relay_pins[relay.toInt()], 1);

  send_status();
}

void turn_off()
{
  String relay = server.arg("relay");
  digitalWrite(relay_pins[relay.toInt()], 0);

  send_status();
}

//=================== SENSORS ====================================
int seconds_delay = 60 * 15;
const int numReadings = 1000;
double send_limit = 400.0;

byte ac1_pin = 12;
const char *ac1_id = "cesspol_indicator";
unsigned long ac1_timer;
int ac1_status;

byte ac1_readings[numReadings];      // the readings from the analog input
int ac1_readIndex = 0;              // the index of the current reading
int ac1_total = 0;                  // the running total
int ac1_average = 0;                // the average

byte ac2_pin = 13;
const char *ac2_id = "auto_magnetic_switcher_indicator";
unsigned long ac2_timer;
int ac2_status;

byte ac2_readings[numReadings];      // the readings from the analog input
int ac2_readIndex = 0;              // the index of the current reading
int ac2_total = 0;                  // the running total
int ac2_average = 0;                // the average


void ac1_Measure() {
  ac1_readIndex = ac1_readIndex + 1;
  // if we're at the end of the array...
  if (ac1_readIndex >= numReadings) {
    // ...wrap around to the beginning:
    ac1_readIndex = 0;
  }

  ac1_readings[ac1_readIndex] = !digitalRead(ac1_pin);
}

bool ac1_CheckIfSend() {
  if (millis() - ac1_timer < seconds_delay * 1000) {
    return false;
  }

  ac1_timer = millis();
  int ac1_sum = 0;
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    ac1_sum = ac1_sum + ac1_readings[thisReading];
  }

  double ac1_avg = ac1_sum / numReadings;
  int ac1_state = int(ac1_avg < send_limit);
  int retry_limit = 5;
  int delay_between_requests = 1000;
//  String req = String(host) + "/api/v1/devices/" + String(device_id) + "/sensors/" + String(ac1_id);
  String req = String(host) + "/api/v1/devices/cesspool";
  for (int i = 1; i <= retry_limit; i++)
  {
    HTTPClient http;

    Serial.println("Sending POST request:");
    Serial.println(req);
    Serial.print(i);
    Serial.print(" try out of ");
    Serial.print(retry_limit);
    Serial.print(". host:");
    Serial.println(host);

    http.begin(req);
    http.addHeader("X-Real-IP", WiFi.localIP().toString());
    http.addHeader("Content-Type", "application/json");
  
//    int httpCode = http.POST("{\"state\":\"" + String(ac1_state) + "\"");         //Send the request
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
}


void ac2_Measure() {
  ac2_readIndex = ac2_readIndex + 1;
  // if we're at the end of the array...
  if (ac2_readIndex >= numReadings) {
    // ...wrap around to the beginning:
    ac2_readIndex = 0;
  }

  ac2_readings[ac2_readIndex] = !digitalRead(ac2_pin);
}


bool ac2_CheckIfSend() {
  if (millis() - ac2_timer < seconds_delay * 1000) {
    return false;
  }

  ac2_timer = millis();
  int ac2_sum = 0;
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    ac2_sum = ac2_sum + ac2_readings[thisReading];
  }

  double ac2_avg = ac2_sum / numReadings;
  int ac2_state = int(ac2_avg < send_limit);
  int retry_limit = 5;
  int delay_between_requests = 1000;
  String req = String(host) + "/data/v1/" + String(device_id) + "/sensors/" + String(ac2_id);

  for (int i = 1; i <= retry_limit; i++)
  {
    HTTPClient http;

    Serial.println("Sending POST request:");
    Serial.println(req);
    Serial.print(i);
    Serial.print(" try out of ");
    Serial.print(retry_limit);
    Serial.print(". host:");
    Serial.println(host);

    http.begin(req);
    http.addHeader("X-Real-IP", WiFi.localIP().toString());
    http.addHeader("Content-Type", "application/json");
  
    int httpCode = http.POST("{\"state\":\"" + String(ac2_state) + "\"");         //Send the request
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
}



//==================== SHARED CODE ===============================
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
      for (JsonVariant v : array) {
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

  previousMillis = millis();
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
  if (int((millis() - current_time) / 60000) >= 30)
  {
    send_ping();
    current_time = millis();
  }
}

void test_relay()
{
  for (byte i = 1; i < num_of_relay; i = i + 1)
  {
    digitalWrite(relay_pins[i], 0);
    delay(1000);
    digitalWrite(relay_pins[i], 1);
    delay(1000);
    digitalWrite(relay_pins[i], 0);
  }

  for (byte i = 1; i < num_of_relay; i = i + 1)
  {
    digitalWrite(relay_pins[i], 1);
  }
  delay(5000);

  for (byte i = 1; i < num_of_relay; i = i + 1)
  {
    digitalWrite(relay_pins[i], 0);
  }
}

void test_system()
{
  send_status();
  test_relay();
}
