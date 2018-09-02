#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266mDNS.h>

byte delay_between_requests = 1000;
byte delay_between_filled_requests = 5000;
int counter = 0;
int counter_max = 300;
int delay_for_counter_millis = 10;
byte retry_limit = 5;

byte TIME_LIMIT_MINUTES = 30;
unsigned long current_time = 0;

const char *host = "http://mozz.asuscomm.com:9000";

String device_id = "weather_station";

//SSID of your network
char ssid[] = "NotebookNet"; //SSID of your Wi-Fi router
char password[] = "0660101327"; //Password of your Wi-Fi router

ESP8266WebServer server(80);

void handleRoot() {
  server.send(200, "application/json", "{\"device_id\": \"" + String(device_id) + "\"");
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

void check_wifi_connection(){
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wait for connection");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  }
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

void setup()
{
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to...");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Wi-Fi connected successfully");

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.onNotFound(handleNotFound);
  server.begin();
}


void loop()
{
  check_wifi_connection();
  server.handleClient();
  send_request(host + String("/weather_station?device_id=") + String(device_id));
  ESP.deepSleep(0.1 * 60 * 1000000); // deepSleep time is defined in microseconds.
  
}
