#include <Wire.h>

String response;
char responseBuf[5] = {'!', '!', '!', '!', '!'};

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
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
  if ((readChar[0] == 'A') && (readChar[1] == 's')){
    responseBuf[0] = 's';
  }
}

void requestEvent(){
  Serial.println(responseBuf);
  Wire.write(responseBuf);
}
