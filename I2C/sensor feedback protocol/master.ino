/* I2C Sensor Feedback Protocol Master Receiver
 * by Saatvik Arya <aryasaatvik@gmail.com>
 *    Armins Stepanjans <>
 *
 * Uses WSWire Library
 * Master Receiver for sensor reading
 * from Slave Sender
 *
 *
 * The circuit: ADXL335
 * A2: z-axis
 * A1: y-axis
 * A0: x-axis
 *
 * Created 20 March 2016
 */

#include <WSWire.h> // import Wire Library

int xpin = A0; // initialise potentiometer pin
int ypin = A1;
int zpin = A2;

void setup() {
  Serial.begin(9600); // begin serial bus
  Wire.begin(); // join i2c bus (address optional for master)
}

void loop() {
  Wire.requestFrom(8, 2);    // request 6 bytes from slave device #8
  while (Wire.available()) { // slave may send less than requested
    byte l = Wire.read(); // receive a byte as character
    byte h = Wire.read();
    Serial.print(word(h,l));
    Serial.print("\n");
  }

  delay(100);
}
