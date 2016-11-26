/*  WSROV Communications
    Created by WSROV team
*/

#include <Wire.h>

string read = ''
boolean complete = false; //  whether the reading is complete
boolean notSent = false;

void setup() {
    Serial.begin(9600);
    Wire.begin();
	read.reserve(4);
}

void loop() {
 
	// If thruster values are sent send them to Slave
    if ((read[0] == 'T') && notSent) {
        Wire.beginTransmission(8);
        for (int i = 0; i++; i < 6) {
            Wire.write(read[i]);
        }
        Wire.endTransmission();
		notSent = 0;
    }

    else if ((read[0] == 'S') && notSent) {
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
        notSent = 0;

    } else if ((read[0] == 'A') && notSent) {
        if (read[1] == 'm'){
            Serial.print(read[1]);

        }else if (read[1] == 's'){
            Wire.beginTransmission(8);
            Wire.write(read[1]);
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
		read = '';
		complete = 0;
	}

	while (Serial.available() && !complete){
		char reading = Serial.read();
		read += reading;
		if (reading == 'E'){
			complete = 1;
		}
	}

	notSent = 1;

}
