/* I2C Led Control Master
 * by Saatvik Arya <aryasaatvik@gmail.com> 
 * 
 * Uses Wire Library
 * Writes potentiometer data to an I2C/TWI slave device
 * to control brightness of a led
 * 
 * Created 16 March 2016
 */
 
#include <WSWire.h>
int ledPin = 9; 
int brightness = 0;
int fadeAmount = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (1 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  int x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
  brightness = x;
  analogWrite(ledPin, brightness);
}
