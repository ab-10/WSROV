/* I2C Led Control Master
 * by Saatvik Arya <aryasaatvik@gmail.com> 
 * 
 * Uses Wire Library
 * Writes potentiometer data to an I2C/TWI slave device
 * to control brightness of a led
 * 
 * Created 16 March 2016
 */
 
#include <WSWire.h> // import Wire Library
int potPin = A2; // initialise potentiometer pin
int raw = 0; // raw reading for potentiometer
int val = 0; // mapped value to potentiometer
void setup() {
  Serial.begin(9600); // begin serial bus
  Wire.begin(); // join i2c bus (address optional for master)
}

void loop() {
  raw = analogRead(potPin); // get raw reading
  val = map(raw, 0, 1023, 0, 255); // map it from 1024 to 256
  Serial.println("potentiometer val: "); 
  Serial.print(val); // print analogread from potentiometer
  Wire.beginTransmission(8); // transmit to device #8
  Wire.write("potentiometer val: ");
  Wire.write(val);              // sends analogread from potentiometer
  Wire.endTransmission();    // stop transmitting
}
