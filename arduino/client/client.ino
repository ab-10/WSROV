#include <DHT.h>
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Servo.h>

byte mac[] = {0x90, 0xA2, 0xDA, 0x0F, 0x16, 0x2F};
IPAddress ip(192, 168, 1, 177);
IPAddress remoteIP(192, 168, 1, 178);
unsigned int localPort = 34;
EthernetUDP Udp;

// Declare parameters and objects for communication with DHT sensor
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

String response;
char responseBuf[5] = {'!', '!', '!', '!', '!'};
int thrusterVals[2] = {1500, 1500};

void setup() {
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);
  dht.begin();
  Serial.begin(9600);
}

void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize > 0){
    receiveEvent(packetSize);
  }
}

void receiveEvent(int howMany) {
  char readChar[howMany];
  Udp.read(readChar, howMany);

  if (readChar[0] == 'T'){
    int value = readChar[1]*100;
    value += readChar[2];
    thrusterVals[0] = value;
    value = readChar[3]*100;
    value += readChar[4];
    thrusterVals[1] = value;

  }else if (readChar[0] == 'S'){
    float reading;
    if (readChar[1] == 't'){
      reading = dht.readTemperature();

    }else if(readChar[1] == 'h'){
      reading = dht.readHumidity();
    }
    Udp.beginPacket(remoteIP, localPort);
    Udp.write(reading);
    Udp.endPacket();

  }else if ((readChar[0] == 'A') && (readChar[1] == 's')){
    Udp.beginPacket(remoteIP, 34);
    Udp.write("s!!!!");
    Udp.endPacket();
  }
}
