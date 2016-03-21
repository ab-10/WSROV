/* I2C Sensor Feedback Protocol Slave Sender
 * by Saatvik Arya <aryasaatvik@gmail.com>
 *    Armins Stepanjans <>
 *
 * Uses WSWire Library
 * Slave Sender for sensor readings
 * to Master Receiver
 *
 * The circuit: ADXL335
 * A2: z-axis
 * A1: y-axis
 * A0: x-axis
 *
 * Created 20 March 2016
 */

#include <WSWire.h> // import Wire Library
int AX,AY,AZ;
int xpin = A0; // initialise potentiometer pin
int ypin = A1;
int zpin = A2;

void setup() {
  Serial.begin(9600);
  Wire.begin(8); // join i2c bus (address optional for master)
  Wire.onRequest(requestEvent);
  AX = analogRead(xpin);
  AY = analogRead(ypin);
  AZ = analogRead(zpin);
}

void loop() {
  Serial.print(AX);
  Serial.print("\t");
  Serial.print(AY);
  Serial.print("\t");
  Serial.print(AZ);
  Serial.print("\n");
  delay(100);
}

void requestEvent() {
  Wire.write(lowByte(AX));
  Wire.write(highByte(AX));
  Wire.write(AZ);
  delay(100);
}
