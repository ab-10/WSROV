/*  WSROV Communications
*   Created by WSROV team
*/

#include <Wire.h>

String reading = "";
boolean complete = false; //  whether the readinging is complete
boolean notSent = false;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    reading.reserve(4);
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
        if (reading[1] == 'h') {
            Wire.write ('h');
            Wire.requestFrom(8, 2);
            int hum = Wire.read();
            hum += Wire.read() / 100;
            Serial.print(hum); 
            Wire.endTransmission();

        }else if (reading[1] == 't'){
            Wire.write ('t');
            Wire.requestFrom(8, 2);
            int temp = Wire.read();
            temp += Wire.read() / 100;
            Serial.print(temp);
            Wire.endTransmission();
        }
        notSent = 0;

    } else if ((reading[0] == 'A') && notSent) {
        if (reading[1] == 'm'){
            Serial.print(reading[1]);

        }else if (reading[1] == 's'){
            Wire.beginTransmission(8);
            Wire.write(reading[1]);
            Wire.requestFrom(8, 2);
            byte c = Wire.read();
            Serial.print(c);
            Wire.endTransmission();
        }
		notSent = 0;
    }
}

void serialEvent() {
	if (complete){
		reading = "";
		complete = 0;
	}

	while (Serial.available() && !complete){
		char inChar = Serial.read();
		reading += inChar;
		if (inChar == 'E'){
			complete = 1;
		}
	}

	notSent = 1;

}
