#include <Wire.h>

int inflowSensor_address = 0x49;
int pressurePin = A7;
int X0,X1,X2,X3;

void setup() {
  Wire.begin();
  Serial.begin(115200);
  delay(100);
}

void loop() {
  if(Serial.available()>0) {
    char val = Serial.read();
    if(val == 'g') {
      readFlow();
      readPressure();
    }
  }
}

void readPressure() {
  int pressureVal = analogRead(pressurePin);
  Serial.println(pressureVal);
}

void readFlow() {
  Wire.requestFrom(inflowSensor_address,2);
  uint16_t flow;
  if (Wire.available() <= 2) {
    int x1 = Wire.read();
    int x2 = Wire.read();
    flow = x1 << 8 | x2;
    Serial.println(getFlowApplied(flow));
  }
}

double getFlowApplied(uint16_t flow) {
  double out = 100*((double(flow)/16384)-0.1)/0.8; // Sensor Transfer Function (Datasheet)
  return out; // out in SLPM
}
