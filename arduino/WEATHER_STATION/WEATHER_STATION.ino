#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

// assign the ESP8266 pins to arduino pins
#define D1 5
#define D2 4
#define D3 0
#define D5 14

// assign the SPI bus to pins
#define BME_SCK D1
#define BME_MISO D5
#define BME_MOSI D2
#define BME1_CS D3

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BMP280 bme1(BME1_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI


byte delay_between_requests = 1000;
byte delay_between_filled_requests = 5000;
int counter = 0;
int counter_max = 300;
int delay_for_counter_millis = 10;
byte retry_limit = 5;
byte conn_retry_limit = 40;

byte TIME_LIMIT_MINUTES = 30;
unsigned long current_time = 0;

int deep_sleep_microsec = 15 * 60 * 1000000;

const char *host = "http://mozz.asuscomm.com:9000";

String device_id = "weather_station";

//SSID of your network
char ssid[] = "NotebookNet"; //SSID of your Wi-Fi router
char password[] = "0660101327"; //Password of your Wi-Fi router

//char ssid[] = "faza_2"; //SSID of your Wi-Fi router
//char password[] = "Kobe_2016"; //Password of your Wi-Fi router

char str_pressure[10], str_temperature[10];

const int numReadings = 10;
int inputPin = A0;

bool check_wifi_connection() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wait for connection");
    WiFi.begin(ssid, password);

    for (int i = 1; i <= conn_retry_limit; i++) {
      if (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      } else {
        Serial.println("");
        Serial.print("Connected to ");
        Serial.println(ssid);
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());

        return true;
      }
    }
    Serial.println("Can't wait till connected.");
    return false;
  }
}

void send_request(String req) {
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
  float p;
  float t;

  analogReference(INTERNAL);
  float avr = 0;
  int sum = 0;
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    sum = sum + analogRead(inputPin);
    delay(100);
  }
  avr = sum / numReadings;

  Serial.begin(115200);

  if (check_wifi_connection() == false){
    Serial.println("Put to sleep.");
    ESP.deepSleep(deep_sleep_microsec); // 15 minutes
  }

  Serial.println(F("BME280 test"));

  bool status;

  // default settings
  status = bme1.begin();
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor. Check wiring!");
  }

  for (byte i = 1; i <= retry_limit; i++) {
    p = bme1.readPressure() / 100.0F;
    Serial.print("Pressure = ");
    Serial.print(p);
    Serial.println(" hPa");
    if (isnan(p)) {
      delay(2000);
    } else {
      break;
    }
  }

  for (byte i = 1; i <= retry_limit; i++) {
    t = bme1.readTemperature();
    Serial.print("Temperature = ");
    Serial.print(t);
    Serial.println(" *C");
    if (isnan(t)) {
      delay(2000);
    } else {
      break;
    }
  }

  dtostrf(p, 1, 2, str_pressure);
  dtostrf(t, 1, 2, str_temperature);

  send_request(host + String("/weather_station?device_id=") + String(device_id) + "&temp=" + String(str_temperature) + "&press=" + String(str_pressure) + "&voltage=" + String(avr));

  ESP.deepSleep(deep_sleep_microsec); // 15 minutes
}

void loop() { }
