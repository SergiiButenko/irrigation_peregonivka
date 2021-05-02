#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266mDNS.h>

byte GPIO_Pin = D6;
int counter = 0;
int counter_max = 300;
int delay_for_counter_millis = 10;

const char *host = "http://mozz.breeze.ua:9000";
const char *serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";

const char *device_id = "upper_tank";
const char *flash_version = "00-00.apr-20-2021";
const char *ssid = "faza_2";
const char *password = "Kobe_2016";

ESP8266WebServer server(80);

void setup()
{
  pinMode(GPIO_Pin, INPUT_PULLUP);

  Serial.begin(115200);
  connect_to_wifi();
  check_wifi_conn();

  server.on("/status", displayDeviceId);
  server.on("/restart", restart_device);
  server.on("/test", displayDeviceId);
  server.on("/device_id", displayDeviceId);
  server.onNotFound(handleNotFound);

  server.on("/", HTTP_GET, []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/html", serverIndex);
  });

  server.on(
      "/update", HTTP_POST, []() {
    server.sendHeader("Connection", "close");
    server.send(200, "text/plain", (Update.hasError()) ? "FAIL" : "OK");
    ESP.restart(); }, []() {
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
    yield(); });
  server.begin();
}

void loop()
{
  check_wifi_conn();
  server.handleClient();

  count_signal(GPIO_Pin);
  if (counter >= counter_max and send_request(host + String("/stop_filling?device_id=") + String(device_id)))
  {
    counter = 0;
  }

  check_if_ping();
}

void increase_counter()
{
  if (counter >= 0 and counter <= counter_max)
  {
    counter++;
    delay(delay_for_counter_millis);
  }
  else
  {
    counter = counter_max;
    delay(delay_for_counter_millis);
  }
}

void decrease_counter()
{
  if (counter >= 1)
  {
    counter--;
  }
  else
  {
    counter = 0;
  }
}

void count_signal(byte pin)
{
  if (digitalRead(pin) == LOW)
  {
    increase_counter();
  }
  else
  {
    decrease_counter();
  }
}

//==================== SHARED CODE ===============================
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
}

void check_wifi_conn()
{
  if (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
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

void check_if_ping()
{
  unsigned long current_time = 0;
  if (int((millis() - current_time) / 60000) >= 30)
  {
    send_ping();
    current_time = millis();
  }
}

bool send_ping()
{
  return send_request(host + String("/im_alive?device_id=") + String(device_id));
}

void startMDNS()
{
  /*use mdns for device_id name resolution*/
  if (!MDNS.begin(device_id, WiFi.localIP())) {
    Serial.println("Error setting up MDNS responder!");
    return;
  }

  Serial.println("mDNS responder started");
  MDNS.addService("http", "tcp", 80);
  Serial.printf("Ready! Open http://%s.local in your browser\n", device_id);
}
