#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

byte MINUTES_TILL_FIRST_PING = 3;

byte GPIO_Pin = D6;

int counter = 0;
int counter_max = 300;
int delay_for_counter_millis = 10;
byte retry_limit = 5;

byte TIME_LIMIT_MINUTES = 30;
unsigned long current_time = 0;

const char *host = "http://mozz.asuscomm.com:7542";
const char *host_https = "https://mozz.asuscomm.com:7542";
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

    for (int i = 1; i <= retry_limit; i++) {
      Serial.println("Initialising http connection");
      HTTPClient http;

      Serial.print("Sending GET request for stop. ");
      Serial.print(i);
      Serial.print(" try out of ");
      Serial.print(retry_limit);
      Serial.print(". Host: ");
      Serial.println(host);
      Serial.println("Sending GET request");

      http.begin(host + String("/stop_filling?device_id=") + String(id));
      int httpCode = http.GET();            //Send the request
      String payload = http.getString();    //Get the response payload

      Serial.print("httpCode: ");
      Serial.println(httpCode);   //Print HTTP return code
      Serial.print("payload: ");
      Serial.println(payload);    //Print request response payload

      http.end();  //Close connection

      if (httpCode == 200) {
        break;
      } else {
        Serial.println("Initialising http connection");
        HTTPClient http;

        Serial.print("Sending GET request for stop. ");
        Serial.print(i);
        Serial.print(" try out of ");
        Serial.print(retry_limit);
        Serial.print(". Host: ");
        Serial.println(host_https);
        Serial.println("Sending GET request");

        http.begin(host_https + String("/stop_filling?device_id=") + String(id));
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
      }

      delay(1000);
    }

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
  for (int i = 1; i <= retry_limit; i++) {
    Serial.println("Initialising http connection for ping");
    HTTPClient http;

    Serial.print("Sending GET request for ping. ");
    Serial.print(i);
    Serial.print(" try out of ");
    Serial.print(retry_limit);
    Serial.print(". host:");
    Serial.println(host);

    http.begin(host + String("/im_alive?device_id=") + String(id));
    int httpCode = http.GET();            //Send the request
    String payload = http.getString();    //Get the response payload

    Serial.print("httpCode: ");
    Serial.println(httpCode);   //Print HTTP return code
    Serial.print("payload: ");
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

    if (httpCode == 200) {
      break;
    } else {
      Serial.println("Initialising https connection for ping");
      HTTPClient http;

      Serial.print("Sending GET request for ping. ");
      Serial.print(i);
      Serial.print(" try out of ");
      Serial.print(retry_limit);
      Serial.print(". host:");
      Serial.println(host_https);
      http.begin(host_https + String("/im_alive?device_id=") + String(id));
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
    }

    delay(1000);
  }

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
