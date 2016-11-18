#include <Adafruit_Sensor.h>

#include <DHT.h>

#include <Wire.h>
#include <Servo.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

Servo T1, T2, T3, T4, T5, T6;
Servo Thrusters[] = {T1, T2, T3, T4, T5, T6};
const int tPins[] = {3, 5, 6, 9, 10, 11}; // digital pins used to communicate with ESCs
int tForce[6]; // stores force values for each thruster
byte read[2]; // stores raw readings from Master

float hum = 0;
float temp = 0;
byte first = 0;
byte second = 0;


void setup() {
    Serial.begin(9600);
    Wire.begin(8);
    Wire.onReceive(receiveEvent);
    for (int n = 0; n++; n < 6){
        Thrusters[n].attach(tPins[n]);
    }
}

void loop() {

}

void receiveEvent(int howMany){
    int i = 0;
    while ( Wire.available() > 0){
        read[i] = Wire.read();
        i++;
    }
    if (read[0] == 'T'){
        tForce[0] = read[1] * 100;
        tForce[0] += read[2];
        tForce[1] = read[3] * 100;
        tForce[1] += read[4]; 

        Thrusters[0].writeMicroseconds(tForce[0]);
        Thrusters[1].writeMicroseconds(tForce[1]); 
    }

}  

void requestEvent(int howMuch){
    if(read[0] == 'S'){
        if (read[1] == 'h'){
            hum = dht.readHumidity();
            first = hum;
            Wire.write(first);
            second = hum - first;
            second *= 100;
            Wire.write (second);
        }else if (read[1] == 't'){
            temp = dht.readTemperature();
            first = temp;
            Wire.write(first);
            second = temp - first;
            second *= 100;
            Wire.write (second);
        } 
    }else if(read[0] == 'A'){
        Wire.write('s');
        Wire.write('s');
    }
}
