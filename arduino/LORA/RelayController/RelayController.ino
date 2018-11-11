#include <SPI.h>
#include <LoRa.h>

const String device_id = "ef6f2d50-f26e-485b-9db6-03fb4a50608c";
bool send_status = false;
const byte relay_quantity = 16;
String operations[] = { "on", "off",  "status" };
byte operations_length = 3;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Receiver");

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  //LoRa.setSyncWord(0xF3);           // ranges from 0-0xFF, default 0x34, see API docs

  // put the radio into receive mode
  LoRa.receive();
  Serial.println("LoRa init succeeded.");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String incoming = "";
    // read packet header bytes:

    for (int i = 0; i < packetSize; i++) {
      incoming += (char)LoRa.read();
    }

    Serial.println("Message: " + incoming);
    Serial.println("RSSI: " + String(LoRa.packetRssi()));
    Serial.println("Snr: " + String(LoRa.packetSnr()));

    char separator = ';';

    /// GET DEVICE ID
    int ind1 = incoming.indexOf(separator);  //finds location of first ,
    if (ind1 == -1) {
      Serial.println("Income message doesn't contain ; separator");
      return;
    }
    String income_device_id = incoming.substring(0, ind1);   //captures first data String
    if ((income_device_id == "") or (income_device_id != device_id)) {
      Serial.println("Income device id is malformed or incorrect");
      return;
    }

    /// GET RECOURSE
    int ind2 = incoming.indexOf(separator, ind1 + 1 ); //finds location of second ,
    if (ind2 == -1) {
      Serial.println("Income message doesn't contain resouce or operation");
      return;
    }

    int relay_num;
    String resource = incoming.substring(ind1 + 1, ind2 + 1); //captures second data String
    if ((resource == "") or (inRange(resource.toInt(), 0, relay_quantity) == -1)) {
      Serial.println("Income relay number is malformed or incorrect");
      return;
    } else {
      relay_num = resource.toInt();
    }


    /// GET OPERATION
    String operation = incoming.substring(ind2 + 1, incoming.length());
    if ( (operation == "") or (arrayContains(operations, operation)) == false ) {
      Serial.println("Income operation is malformed or incorrect");
      return;
    }

    execute(relay_num, operation);
    sendStatus();
  }
}

void execute(byte relay_num, String operation) {
  //  relay_num = relay_num - 1;
  //  digitalWrite(relay_num, operation);
  Serial.println("done");
}

void sendStatus() {
  String outgoing = device_id;
  outgoing += ';';

  for (byte i = 0; i < relay_quantity; i++) {
    outgoing += digitalRead(i);
  }
  Serial.println("Sending back: ");
  Serial.println(outgoing);
  delay(100);
  LoRa.beginPacket();                   // start packet
  LoRa.print(outgoing);                 // add payload
  LoRa.endPacket();                     // finish packet and send it
  delay(100);
  
  LoRa.receive();
}

//// HELPERS ////
bool arrayContains(String arr[], String el) {
  for (byte i = 0; i < operations_length; i++) {
    if (arr[i] == el) {
      return true;
      break;
    }
  }

  return false;
}

byte inRange(byte val, int minimum, int maximum)
{
  if ((val >= minimum) && (val <= maximum) ) {
    return val;
  }

  return -1;
}
