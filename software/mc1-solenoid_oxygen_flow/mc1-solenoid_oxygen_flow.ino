#include <Wire.h>

int inhaleSolenoidPin = 8;
int exhaleSolenoidPin = 7;
int oxygenPin = A7;
int inhale = 3000;
int exhale = 2000;
bool isInhale = true;
int outflowSensor_address = 0x49;
int X0,X1,X2,X3;

void setup() {
  Wire.begin();
  Serial.begin(115200);
  delay(100);
  pinMode(inhaleSolenoidPin, OUTPUT);
  pinMode(exhaleSolenoidPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if(Serial.available()>0) {
    char val = Serial.read();
    if(val == 'g') {
      readFlow();
      readOxygen();
    } else if (val == 'i') {
      digitalWrite(inhaleSolenoidPin, HIGH);
      digitalWrite(exhaleSolenoidPin, LOW);
      digitalWrite(LED_BUILTIN, HIGH);
      isInhale = true;
    } else if (val == 'e') {
      digitalWrite(inhaleSolenoidPin, LOW);
      digitalWrite(exhaleSolenoidPin, HIGH);
      digitalWrite(LED_BUILTIN, LOW);
      isInhale = false;      
    }
  }
}

void readOxygen() {
  int oxygenVal = analogRead(oxygenPin);
  Serial.println(oxygenVal);
}

void readOxygenDebug() {
  int oxygenVal = analogRead(oxygenPin);
  double fio2 = ((oxygenVal-204.6)/818.4) * 100;
  Serial.println(fio2);
}
void readFlow() {
  Wire.requestFrom(outflowSensor_address,2);
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
