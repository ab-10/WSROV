#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Servo.h>

String response;
char responseBuf[5] = {'!', '!', '!', '!', '!'};
int thrusterVals[2] = {1500, 1500};

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.setClock(500);
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  Serial.begin(9600);           // start serial for output
}

void loop() {
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  char readChar[howMany];
  Wire.readBytes(readChar, howMany);
  if (readChar[0] == 'T'){
    int value = readChar[1]*100;
    value += readChar[2];
    thrusterVals[0] = value;
    value = readChar[3]*100;
    value += readChar[4];
    thrusterVals[1] = value;

  }else if ((readChar[0] == 'A') && (readChar[1] == 's')){
    responseBuf[0] = 's';
  }
}

void requestEvent(){
  Serial.println(responseBuf);
  Wire.write(responseBuf);
}
