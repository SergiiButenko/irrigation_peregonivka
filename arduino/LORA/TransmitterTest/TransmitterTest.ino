#include <SPI.h>
#include <LoRa.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {


  Serial.println("ef6f2d50-f26e-485b-9db6-03fb4a50608c;6;on");
  LoRa.beginPacket();
  LoRa.print("ef6f2d50-f26e-485b-9db6-03fb4a50608c;6;on");
  LoRa.endPacket();
  delay(100);
  LoRa.receive();
  
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }

    // print RSSI of packet
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());
  }
  
  delay(5000);
}
