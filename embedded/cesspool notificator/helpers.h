#include "settings.h"

unsigned long currentMillis = 0;
unsigned long previousMillis = 0;

ESP8266WebServer server(80);
const char* serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";


void displayDeviceId() {
  String msg = "{";
  msg += "\"device_id\":\"" + String(device_id) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.sendHeader("X-Real-IP", WiFi.localIP());
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
}


void restart_device() {
  server.sendHeader("X-Real-IP", WiFi.localIP());
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", "restarted");
  ESP.restart();
}


void displayVersion() {
  String msg = "{";
  msg += "\"flash_version\":\"" + String(flash_version) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.sendHeader("X-Real-IP", WiFi.localIP());
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
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

  server.sendHeader("X-Real-IP", WiFi.localIP());
  server.sendHeader("Connection", "close");
  server.send(404, "text/plain", message);
}

void scan_wifi() {
  Serial.println("Scan start");

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("Scan done");
  if (n == 0) {
    Serial.println("Error: No networks found");
    return;
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
      delay(10);
    }
  }
  Serial.println("");
}

void wait_wifi_conn() {
  // Wait for connection
  WiFi.hostname(device_id);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
  }
  
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    delay(1000);
  }

  String req = host + String("/im_alive?device_id=") + String(device_id);
  while (send_request(req))
  {
    delay(registration_interval);
  }
}

void test_system() {
  send_status();
  scan_wifi();
}

bool send_request(String req) {
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
    http.addHeader("X-Real-IP", WiFi.localIP());

    int httpCode = http.GET();            //Send the request
    String payload = http.getString();    //Get the response payload

    Serial.print("httpCode: ");
    Serial.println(httpCode);   //Print HTTP return code
    Serial.print("payload: ");
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

    if (httpCode == 200) {
      return true;
    }

    delay(delay_between_requests);
  }

  return false;
}

