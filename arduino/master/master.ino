/*  WSROV Communications
*   Created by WSROV team
*/

#include <Wire.h>

byte reading[6];
boolean complete = false; //  whether the readinging is complete
boolean notSent = false;
int n = 0;

void setup() {
    Serial.begin(9600);
    Wire.begin();
}

void loop() {
 
	// If thruster values are sent send them to Slave
    if ((reading[0] == 'T') && notSent) {
        Wire.beginTransmission(8);
        for (int i = 0; i++; i < 6) {
            Wire.write(reading[i]);
        }
        Wire.endTransmission();
		notSent = 0;
    }

    else if ((reading[0] == 'S') && notSent) {
        Wire.beginTransmission(8);
        for(int i = 0; i++; i < 6) {
            Wire.write(reading[i]);
        }
        Wire.requestFrom(8, 2);
        byte wholePart = Wire.read();
        byte decimalPart = Wire.read();
        Serial.print(wholePart);
        Serial.print(decimalPart);
        Wire.endTransmission();

        notSent = 0;

    } else if ((reading[0] == 'A') && notSent) {
        if (reading[1] == 'm'){
            notSent = 0;
            Serial.print(reading[1]);

        }else if (reading[1] == 's'){
            Wire.beginTransmission(8);
            for(int i = 0; i++; i < 6){
                Wire.write(reading[i]);
            }
            Wire.requestFrom(8, 1);
            byte response = Wire.read();
            Serial.print(response);
            Wire.endTransmission();
        }
    }
}

void serialEvent() {
	if (complete){
		complete = 0;
        n = 0;
	}

	while (Serial.available() && !complete){
		byte inByte = Serial.read();
		reading[n] = inByte;
        n ++;
		if (inByte == 'E'){
			complete = 1;
            n = 0;
            notSent = 1;
		} else if(n > 5){
            n = 0;
        }
	}

	notSent = 1;

}
