#include <SoftwareSerial.h>
#include <Servo.h>
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

byte mac[] = {0x90, 0xA2, 0xDA, 0x0D, 0xD2, 0x92};
IPAddress ip(192, 168, 1, 178);
IPAddress remoteIP(192, 168, 1, 177);
unsigned int localPort = 34;
EthernetUDP Udp;

SoftwareSerial *sserial = NULL;
Servo servos[8];
int servo_pins[] = {0, 0, 0, 0, 0, 0, 0, 0};
boolean connected = false;

void setup()  {
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()){
    SerialParser();
  }
}

int Str2int (String Str_value){
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

void SerialParser() {
  char readChar[10];
  String read_;
  Serial.readBytesUntil('E',readChar, 10);
  read_ = String(readChar);
  char header = readChar[0];
  if (header == 'T'){
    // Change thruster values
    Serial.println('T');
  } else if (header == 'S'){
    Serial.println("10");
    /*
    // Request sensor values from Slave and send them to Main
    Udp.beginPacket(remoteIP, localPort);
    Udp.write(readChar);
    Udp.endPacket();
    unsigned long time = millis();
    while((Udp.parsePacket() < 1) && (millis()-time < 1000)){
      ;
    }
    Udp.read(readChar, 10);
    Serial.println(readChar);
    */
  } else if (header == 'A'){
    // Respond to the ping
    if (readChar[1] == 'm'){
      Serial.println('m');
    } else if(readChar[1] == 's'){
      Udp.beginPacket(remoteIP, localPort);
      Udp.write(readChar);
      Udp.endPacket();
      unsigned long time = millis();
      while((Udp.parsePacket() < 1) && (millis()-time < 1000)){
        ;
      }
      Udp.read(readChar, 10);
      if (readChar[0] == 's'){
        Serial.println('s');
      }
    }
  }
}
