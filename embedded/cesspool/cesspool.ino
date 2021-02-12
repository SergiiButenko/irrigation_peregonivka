#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266mDNS.h>

byte GPIO_Pin = D6;

byte delay_between_requests = 1000;
byte delay_between_filled_requests = 5000;
int counter = 0;
int counter_max = 300;
int delay_for_counter_millis = 10;
byte retry_limit = 5;
unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval = 1000 * 60 * 15;           // interval at which to blink (milliseconds)

byte TIME_LIMIT_MINUTES = 30;
unsigned long current_time = 0;

const char *host = "http://irrigation.faza:9000/api/v1";

String device_id = "cesspool";

const char* ssid = "faza_2";
const char* password = "Kobe_2016";

ESP8266WebServer server(80);

void handleRoot() {
  server.send(200, "application/json", "{\"device_id\": \"" + String(device_id) + "\", \"counter\":" + String(counter) + "}");
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


void setup() {
  Serial.begin(115200);
  Serial.println("Setup");

  pinMode(GPIO_Pin, INPUT_PULLUP);

  Serial.begin(115200);
  WiFi.setAutoConnect(true);
  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  Serial.println("Finished");

  Serial.println("Wait for connection");
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

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.onNotFound(handleNotFound);
  server.begin();

  send_ping();
}

void loop() {
  check_wifi_connection();
  server.handleClient();
  
  unsigned long currentMillis = millis();
  if ((currentMillis - previousMillis >= interval) and (counter >= counter_max)) {
    previousMillis = currentMillis;
    send_request(host + String("/cesspool"));
    
    counter = 0;
    delay(delay_between_filled_requests);
  }

  ping();
  count_signal();
}

void count_signal() {
  if (digitalRead(GPIO_Pin) == LOW) {
    increase_counter();
  } else {
    decrease_counter();
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

void increase_counter() {
  if (counter >= 0 and counter <= counter_max) {
    counter++;
    delay(delay_for_counter_millis);
  } else {
    counter = counter_max;
    delay(delay_for_counter_millis);
  }
}

void decrease_counter() {
  if (counter >= 1) {
    counter--;
  } else {
    counter = 0;
  }
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
