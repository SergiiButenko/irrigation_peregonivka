#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "DHT.h"
 
#define DHTPIN D2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

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

DHT dht(DHTPIN, DHTTYPE);
char str_humidity[10], str_temperature[10];

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
  delay(2000);

  check_wifi_connection();
  dht.begin();
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  dtostrf(h, 1, 2, str_humidity);
  dtostrf(t, 1, 2, str_temperature);

  send_request(host + String("/weather_station?device_id= \"") + String(device_id) + "\"&temp=" + String(str_temperature) + "&hum=" + String(str_humidity));
  ESP.deepSleep(20e6); // 20e6 is 20 microseconds
}

void loop() { }
