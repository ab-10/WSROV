#include <DHT.h>
#include <DHT_U.h>

#include <Wire.h>
#include <Servo.h>

#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

Servo T1, T2, T3, T4, T5, T6;
Servo Thrusters[] = {T1, T2, T3, T4, T5, T6};
const int tPins[] = {3, 5, 6, 9, 10, 11}; // digital pins used to communicate with ESCs
int tForce[6]; // stores force values for each thruster
byte read; // stores raw readings from Master

float hum = 0;
float temp = 0;
byte first = 0;
byte second = 0;
int i = 0;


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

void receiveEvent(int howMany){
  while(Wire.available()){
    read = Wire.read();
    
    if (read == 1){
      hum = dht.readHumidity();
      first = hum;
      Wire.write(first);
      second = hum - first;
      second *= 100;
      Wire.write (second);
    }

    if (read == 2){
      temp = dht.readTemperature();
      first = temp;
      Wire.write(first);
      second = temp - first;
      second *= 100;
      Wire.write (second);
    }
  }
}
void requestEvent(int howMuch){
     Wire.write(3);
     Wire.write(3);
  }
