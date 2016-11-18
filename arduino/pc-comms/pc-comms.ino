/*  WSROV Communications
    Created by WSROV team
*/

#include <Wire.h>

char read[20];
boolean notSent;

void setup() {
    Serial.begin(9600);
    Wire.begin();
}

void loop() {
    if (Serial.available() > 0){
        notSent = true;
    }
    Serial.readBytesUntil('E', read, 20);
    // If thruster values are sent send them to Slave
    if (read[0] == 'T') {
        Wire.beginTransmission(8);
        for (int i = 0; i++; i < 6) {
            Wire.write(read[i]);
        }
        Wire.endTransmission();
    }
    else if ((read[0] == 'S') && notSent){
        Wire.beginTransmission(8);
        if (read[1] == 'h') {
            Wire.write ('h');
            Wire.requestFrom(8, 2);
            int hum = Wire.read();
            hum += Wire.read() / 100;
            Serial.print(hum); 
            Wire.endTransmission();
        }else if (read[1] == 't'){
            Wire.write ('t');
            Wire.requestFrom(8, 2);
            int temp = Wire.read();
            temp += Wire.read() / 100;
            Serial.print(temp);
            Wire.endTransmission();
        }
        notSent = false;
    } else if (read[0] == 'A'){
        if (read[1] == 'm'){
            Serial.print(read[2]);
        }else if (read[1] == 's'){
            Wire.beginTransmission(8);
            Wire.write(read[1]);
            Wire.requestFrom(8, 2);
            byte c = Wire.read();
            Serial.print(c);
            Wire.endTransmission();
        }
    }
}
