#include <Wire.h>
#include <Servo.h>
#include <DHT.h>

#define DHTPIN 2     
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

String response;
char responseBuf[5] = {'!', '!', '!', '!', '!'};
int thrusterVals[2] = {1500, 1500};

byte hum;
byte temp;
float realtemp;
float realhum;

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.setClock(500);
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  Serial.begin(9600);           // start serial for output
  dht.begin();
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
    
  }else if (readChar[0] == 'S') {
        if (readChar[1] == 't'){
         realtemp = dht.readTemperature();
         temp = realtemp;
         responseBuf[0] = temp;
         realtemp = realtemp - temp;
         temp = realtemp * 100; 
         responseBuf[1] = temp;
    }
        else if (readChar[1] == 'h'){
         realhum = dht.readHumidity();
         hum = realhum;
         responseBuf[0] = hum;
         realhum = realhum - hum;
         hum = realhum * 100;
         responseBuf[1] = hum;
    }
   }
}
void requestEvent(){
  Serial.println(responseBuf);
  Wire.write(responseBuf);
}
