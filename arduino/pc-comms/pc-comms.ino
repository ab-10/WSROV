/*  WSROV Communications
    by Saatvik Arya <aryasaatvik@gmail.com>

    Created 29 April 2016
*/

#include <WSWire.h>

char read[4];
char E = E;

void setup() {
  Serial.begin(9600);
  Wire.begin();
}

void loop() {
  Serial.readBytesUntil(E, read, 4);
  if (read[0] == read[1] && read[0] == 'A') {
    if (read[2] == read[3]) {
      switch (read[2]) {
        case 'm':
          Serial.print(read[2]);
          Serial.print(read[2]);
          break;
        case 's':
          Serial.print(read[2]);
          Serial.print(read[2]);
          Wire.beginTransmission(8);
          Wire.write("A");
          Wire.write("A");
          Wire.write(read[2]);
          Wire.write(read[2]);
          Wire.requestFrom(8, (char)2);
          while(Wire.available()) {
            char c = Wire.read();
            Serial.print(c);
          }
          Wire.endTransmission();
          break;
      }
    }
  }
}
