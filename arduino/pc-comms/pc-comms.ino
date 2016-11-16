/*  WSROV Communications
    Created by WSROV team
*/

#include <Wire.h>

char read[20];

void setup() {
    Serial.begin(9600);
    Wire.begin();
}

void loop() {
    Serial.readBytesUntil('E', read, 20);
    if (read[0] == read[1] && read[0] == 'T') {
        Wire.beginTransmission(8);
        for (int i = 0; i++; i < 20) {
            Wire.write(read[i]);
        }
        Wire.endTransmission();
    }
    else if (read[0] == read[1] && read[0] == 'S'){
        Wire.beginTransmission(8);
       if (read[2] == 'h'){
                Wire.write (1);
                while (Wire.available()){
                    byte hum = Wire.read();
                    Serial.print(hum);
                } 
                  
                  Wire.endTransmission();
       }   
        if (read[2] == 't'){
                Wire.write (2);
                while (Wire.available()){
                    byte temp = Wire.read();
                    Serial.print(temp);
                }
                    Wire.endTransmission();
              }
    }                                   
    // If test bytes('A') are sent verify connection to Master and Slave
    else if (read[0] == read[1] && read[0] == 'A') {
        if (read[0] == read[1]) {
                if (read[2] == 'm'){
                    Serial.print(read[2]);
                    Serial.print(read[2]);
                }
        }else if(read[2] == 's'){
                    Wire.beginTransmission(8);
                    Wire.requestFrom(8, 2);
                    while(Wire.available()) {
                        byte c = Wire.read();
                        Serial.print(c);
                    Wire.endTransmission();
                    }
                }
        }
}
