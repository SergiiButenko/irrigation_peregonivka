#include "settings.h"


ESP8266WebServer server(80);
const char* serverIndex = "<form method='POST' action='/update' enctype='multipart/form-data'><input type='file' name='update'><input type='submit' value='Update'></form>";


void displayDeviceId() {
  String msg = "{";
  msg += "\"device_id\":\"" + String(device_id) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
}


void restart_device() {
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", "restarted");
  ESP.restart();
}

void displayVersion() {
  String msg = "{";
  msg += "\"flash_version\":\"" + String(flash_version) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
}

void send_status() {
  String msg = "{";
  for (byte i = 1; i < num_of_relay - 1; i = i + 1) {
    msg += "\"" + String(i) + "\":\"" + String(digitalRead(relay_pins[i])) + "\",";
  }
  msg += "\"" + String(num_of_relay - 1) + "\":\"" + String(digitalRead(relay_pins[num_of_relay - 1])) + "\"";
  msg += "}";

  Serial.println("Message to send:" + msg);
  server.sendHeader("Connection", "close");
  server.send(200, "application/json", msg);
}

void turn_on() {
  String relay = server.arg("relay");
  digitalWrite(relay_pins[relay.toInt()], 1);

  send_status();
}

void turn_off() {
  String relay = server.arg("relay");
  digitalWrite(relay_pins[relay.toInt()], 0);

  send_status();
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
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(1000);
    ESP.restart();
  }
}

void test_relay() {
  for (byte i = 1; i < num_of_relay; i = i + 1) {
    digitalWrite(relay_pins[i], 0);
    delay(1000);
    digitalWrite(relay_pins[i], 1);
    delay(1000);
    digitalWrite(relay_pins[i], 0);
  }
}

void test_system() {
  send_status();

  test_relay();
  scan_wifi();
}
// ===================================== SWITCHER ========================================
void increase_counter(int *counter) {
  if (*counter >= 0 and * counter <= counter_max) {
    *counter++;
    delay(delay_for_counter_millis);
  } else {
    *counter = counter_max;
    delay(delay_for_counter_millis);
  }
}

void decrease_counter(int *counter) {
  if (*counter >= 1) {
    *counter--;
  } else {
    *counter = 0;
  }
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

void handleSwitchers(void) {
  for (byte i = 1; i < num_of_switcher; i = i + 1) {
    byte curr_state = digitalRead(switcher_pins[i]);
    Serial.println("");
    Serial.println("");
    Serial.print("prev: ");
    Serial.println(switcher_state[i]);

    Serial.print("curr: ");
    Serial.println(curr_state);

    Serial.print("pin: ");
    Serial.println(switcher_pins[i]);

    Serial.print("counter: ");
    Serial.println(switcher_counter[i]);

    if (curr_state != switcher_state[i]) {
      if (switcher_counter[i] <= counter_max) {
        switcher_counter[i]++;
        delay(delay_for_counter_millis);
      }
    } else {
      if (switcher_counter[i] >= 1) {
        switcher_counter[i]--;
        delay(delay_for_counter_millis);
      }
    }

    if (switcher_counter[i] >= counter_max) {
      Serial.println(switcher_counter[i]);

      String url = host;
      url += String("/toogle_line?device_id=") + String(device_id) + String("&");
      url += String("switch_num=") + String(i);
      send_request(url);
      
      switcher_state[i] = curr_state;
      switcher_counter[i] = 0;
    }
  }


}
