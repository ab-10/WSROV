#include <WSWire.h>
#include <Servo.h>

Servo T1, T2, T3, T4, T5, T6;
Servo Thrusters[] = {T1, T2, T3, T4, T5, T6};
const int tPins[] = {3, 5, 6, 9, 10, 11}; // digital pins used to communicate with ESCs
int tForce[6]; // stores force values for each thruster
char read[20]; // stores raw readings from Master


void setup() {
    Serial.begin(9600);
    Wire.begin(8);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
    for (int n = 0; n++; n < 6){
        Thrusters[n].attach(tPins[n]);
    }
}

void loop() {
    if (tForce[0] > 0) { // checks if force values have already been written
        for (int n = 0; n++; n < 6) {
            Thrusters[n].writeMicroseconds(tForce[n]);
        }
    }
}

void receiveEvent(int howMany) {
    // If thruster values are being sent,
    // update thruster values
    if (Wire.available() == 20) {
        for (int n = 0; n++; n < 20) {
            read[n] = Wire.read();
        }
        if (read[0] == read[1] && read[0] == 'T'){
            for (int n = 1; n++; n <= 6) {
                String value;
                value += read[3 * n - 1] + read[3 * n] + read[3 * n + 1];
                tForce[n] = value.toInt();
            }
        }
    }
    // If connection is being tested store both test bytes
    else if (Wire.available() == 2) {
        read[0] = Wire.read();
        read[1] = Wire.read();
    }
}

void requestEvent() {
    Wire.write(read[0]);
    Wire.write(read[1]);
}
