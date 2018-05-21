#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

byte GPIO_Pin = D6;

int counter = 0;
int counter_max = 300;
int delay_for_counter_millis = 10;
byte ping_send_status = 0;
byte report_send_status = 0;

byte TIME_LIMIT_MINUTES = 30;
unsigned long current_time = 0;

const char *host = "http://mozz.asuscomm.com:7542";
String id = "upper_tank";

//const char* ssid = "NotebookNet";
//const char* password = "0660101327";
const char* ssid = "faza_2";
const char* password = "Kobe_2016";



void setup() {
  Serial.begin(115200);
  Serial.println("Setup");

  pinMode(GPIO_Pin, INPUT_PULLUP);

  Serial.begin(115200);
  WiFi.setAutoConnect (true);
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

  send_ping();
}

void loop() {
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

  if (counter >= counter_max) {
    Serial.println(counter);
    Serial.println(counter >= counter_max);

    Serial.println("Initialising http connection");
    HTTPClient http;

    Serial.println("Sending GET request");
    http.begin(host + String("/stop_filling?device_id=") + String(id));
    int httpCode = http.GET();            //Send the request
    String payload = http.getString();    //Get the response payload

    Serial.print("httpCode: ");
    Serial.println(httpCode);   //Print HTTP return code
    Serial.print("payload: ");
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

    counter = 0;
    delay(5000);
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
  }
}


void send_ping() {
  Serial.println("Initialising http connection for ping");
  HTTPClient http;

  Serial.println("Sending GET request for ping");
  http.begin(host + String("/im_alive?device_id=upper_tank"));
  int httpCode = http.GET();            //Send the request
  String payload = http.getString();    //Get the response payload

  Serial.print("httpCode: ");
  Serial.println(httpCode);   //Print HTTP return code
  Serial.print("payload: ");
  Serial.println(payload);    //Print request response payload

  http.end();  //Close connection

  current_time = millis();
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


