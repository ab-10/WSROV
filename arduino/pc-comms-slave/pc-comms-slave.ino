#include <WSWire.h>
char read[4];
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin(8);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void receiveEvent(int howMany) {
  if(Wire.available() == 4){
    read[0] = Wire.read();
    read[1] = Wire.read();
    read[2] = Wire.read();
    read[3] = Wire.read();
  }
  char c = Wire.read();
  Serial.print(c);
}

void requestEvent() {
  Wire.write(read[0]);
  Wire.write(read[1]);
  Wire.write(read[2]);
  Wire.write(read[3]);
}

