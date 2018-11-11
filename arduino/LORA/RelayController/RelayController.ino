#include <SPI.h>
#include <LoRa.h>

String device_id = "ef6f2d50-f26e-485b-9db6-03fb4a50608c";
bool send_status = false;
byte relay_number = 16;

void setup() {
id setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Receiver");
  Serial.println(device_id);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  
  LoRa.setSyncWord(0xF3);           // ranges from 0-0xFF, default 0x34, see API docs
  
  // register the receive callback
  LoRa.onReceive(onReceive);

  // put the radio into receive mode
  //LoRa.receive();
  Serial.println("LoRa init succeeded.");
}

void loop() {
  // try to parse packet
  if (send_status == true) {
    sendStatus();
  }
}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return
  
  String incoming = "";
  // read packet header bytes:
 
  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }
 
  Serial.println("Message: " + incoming);
  Serial.println("RSSI: " + String(LoRa.packetRssi()));
  Serial.println("Snr: " + String(LoRa.packetSnr()));
  Serial.println();

  if validateIncome(incomming) {
    execute(relay_num, operation);
    send_status = true;
  } else {
    Serial.println("Message is not valid!");
  }
}

bool validateIncome(String incomming){
  
}

void execute(byte relay_num, byte operation){
  relay_num = relay_num - 1;
  digitalWrite(relay_num, operation);
}

void sendStatus() {
  String outgoing = device_id;
  outgoing += 
  
  LoRa.beginPacket();                   // start packet
  LoRa.print(outgoing);                 // add payload
  LoRa.endPacket();                     // finish packet and send it
  
}
