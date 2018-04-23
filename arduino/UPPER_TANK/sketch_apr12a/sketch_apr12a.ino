uint8_t GPIO_Pin = D7;

void setup() {
 Serial.begin(9600);
 Serial.println(millis());
 Serial.println("started");
 attachInterrupt(digitalPinToInterrupt(GPIO_Pin), IntCallback, RISING);
}

void loop() {
}

void IntCallback(){
 Serial.print("Stamp(ms): ");
 Serial.println(millis());
}
