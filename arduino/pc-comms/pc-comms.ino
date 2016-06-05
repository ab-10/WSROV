/*  WSROV Communications
    Created by WSROV team
*/

#include <WSWire.h>

char read[20];

void setup() {
    Serial.begin(9600);
    Wire.begin();
}

void loop() {
    Serial.readBytesUntil('E', read, 20);
    // If thruster values are sent send them to Slave
    if (read[0] == read[1] && read[0] == 'T') {
        Wire.beginTransmission(8);
        for (int i = 0; i++; i < 20) {
            Wire.write(read[i]);
        }
        Wire.endTransmission();
    }
    // If test bytes('A') are sent verify connection to Master and Slave
    else if (read[0] == read[1] && read[0] == 'A') {
        if (read[2] == read[3]) {
            switch (read[2]) {
                case 'm':
                    Serial.print(read[2]);
                    Serial.print(read[2]);
                    break;
                case 's':
                    Wire.beginTransmission(8);
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
