#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Servo.h>

byte mac[] = {0x90, 0xA2, 0xDA, 0x0F, 0x16, 0x2F};
IPAddress ip(192, 168, 1, 177);
IPAddress remoteIP(192, 168, 1, 178);
unsigned int localPort = 34;

String response;
char responseBuf[5] = {'!', '!', '!', '!', '!'};
int thrusterVals[2] = {1500, 1500};

void setup() {
  Ethernet.begin(mac, ip);
  EthernetUdp.begin(localPort);

  Serial.begin(9600);
}

void loop() {
  int packetSize = EthernetUdp.parsePacket();
  if (packetSize > 0){
    receiveEvent(packetSize);
  }
}

void receiveEvent(int howMany) {
  char readChar[howMany];
  EthernetUdp.read(readChar, howMany);

  if (readChar[0] == 'T'){
    int value = readChar[1]*100;
    value += readChar[2];
    thrusterVals[0] = value;
    value = readChar[3]*100;
    value += readChar[4];
    thrusterVals[1] = value;

  }else if ((readChar[0] == 'A') && (readChar[1] == 's')){
    EthernetUdp.beginPacket(remoteIP, 34);
    EthernetUdp.write("s!!!!");
    EthernetUdp.endPacket();
  }
}

void requestEvent(){
  Serial.println(responseBuf);
  Wire.write(responseBuf);
}
