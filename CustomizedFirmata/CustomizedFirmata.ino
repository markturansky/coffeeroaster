#include <Firmata.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include "max6675.h"

byte previousPIN[TOTAL_PORTS];  // PIN means PORT for input
byte previousPORT[TOTAL_PORTS];

// custom firmata sysEx commands to send thermo data back to waiting firmata client
#define THERMO_ENV              0x0A
#define THERMO_BEAN             0x0B

#define BACKLIGHT_PIN     13

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

int thermoDO = 4; // shared by all thermocouplers
int beanCS = 5; // CS is distinct for each thermocoupler
int thermoCLK = 6; // shared by all thermocouplers
int environmentCS = 7; // CS is distinct for each thermocoupler

MAX6675 beanThermo(thermoCLK, beanCS, thermoDO);
MAX6675 envThermo(thermoCLK, environmentCS, thermoDO);

void outputPort(byte portNumber, byte portValue)
{
  // only send the data when it changes, otherwise you get too many messages!
  if (previousPIN[portNumber] != portValue) {
    Firmata.sendDigitalPort(portNumber, portValue);
    previousPIN[portNumber] = portValue;
  }
}

void setPinModeCallback(byte pin, int mode) {
  if (IS_PIN_DIGITAL(pin)) {
    pinMode(PIN_TO_DIGITAL(pin), mode);
  }
}

void digitalWriteCallback(byte port, int value)
{
  byte i;
  byte currentPinValue, previousPinValue;

  if(port == 4 || port == 5 || port == 6 || port == 7){
    // ignore these pins. they are used for the thermocouplers 
    // and do not receive digital input.
  }

  if (port < TOTAL_PORTS && value != previousPORT[port]) {
    for (i = 0; i < 8; i++) {
      currentPinValue = (byte) value & (1 << i);
      previousPinValue = previousPORT[port] & (1 << i);
      if (currentPinValue != previousPinValue) {
        digitalWrite(i + (port * 8), currentPinValue);
      }
    }
    previousPORT[port] = value;
  }
}

void setup()
{
  lcd.begin(16,2);
  lcd.backlight();

  lcd.clear();
  lcd.home ();
  lcd.print("GrovesCoffeeCo");
  lcd.setCursor(0, 1);
  lcd.print("version 2.0");
  delay(400);
  
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);
  Firmata.attach(DIGITAL_MESSAGE, digitalWriteCallback);
  Firmata.attach(SET_PIN_MODE, setPinModeCallback);
  Firmata.begin(57600);
}

void loop()
{
  int beanTemp = beanThermo.readFahrenheit();
  int envTemp = envThermo.readFahrenheit();
  
  lcd.clear();
  lcd.home();
  lcd.print("ET: ");
  lcd.print(envTemp);
  lcd.setCursor(0, 1);
  lcd.print("BT: ");
  lcd.print(beanTemp);

  byte envTempBytes[4];
  byte beanTempBytes[4];

  *((int *)envTempBytes) = envTemp;
  *((int *)beanTempBytes) = beanTemp;
    
  Firmata.sendSysex(THERMO_ENV, 4, envTempBytes);
  Firmata.sendSysex(THERMO_BEAN, 4, beanTempBytes);
   
  byte i;

  for (i = 0; i < TOTAL_PORTS; i++) {
    outputPort(i, readPort(i, 0xff));
  }

  while (Firmata.available()) {
    Firmata.processInput();
  }

  delay(500);
}
