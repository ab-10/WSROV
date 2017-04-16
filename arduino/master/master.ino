#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h>
#include <EEPROM.h>

SoftwareSerial *sserial = NULL;
Servo servos[8];
int servo_pins[] = {0, 0, 0, 0, 0, 0, 0, 0};
boolean connected = false;

int Str2int (String Str_value)
{
  char buffer[10]; //max length is three units
  Str_value.toCharArray(buffer, 10);
  int int_value = atoi(buffer);
  return int_value;
}

void split(String results[], int len, String input, char spChar) {
  String temp = input;
  for (int i=0; i<len; i++) {
    int idx = temp.indexOf(spChar);
    results[i] = temp.substring(0,idx);
    temp = temp.substring(idx+1);
  }
}

void Version(){
  Serial.println("version");
}

void SerialParser() {
  char readChar[10];
  String read_;
  Serial.readBytesUntil('E',readChar,64);
  read_ = String(readChar);
  char header = readChar[0];
  if (header == 'T'){
    // Change thruster values
    Serial.println('T');
  } else if (header == 'S'){
    // Request sensor values from Slave and send them to Main
    Serial.println('S');
  } else if (header == 'A'){
    // Respond to the ping
    if (readChar[1] == 'm'){
      Serial.println('m');
    } else if (readChar[1] == 's'){
      // Check connection with Slave
      Serial.println('s');
    }
  }
}

void setup()  {
  Serial.begin(9600);
    while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
}

void loop() {
  if (Serial.available()){
    SerialParser();
  }
}
