/*
 code projet drone nautique lejoola 
@author:khadim mbacke ndiaye 
*/
#include <Wire.h>
#include <LCD03.h>
#include <ESPServo.h>
#include "ESC.h"


#define ESC_PIN(33)
#define LED_BUILTIN(2)
#define POT_PIN(34)
#define MIN_SPEED 1040
#define PMAX_SPEED 1240
ESC myESC(ESC_PIN,1000,2000,500);
long int val;
LCD03 lcd;
 
void setup() {
  serial.begin(96000);
  delay(1000);
  pinMode(POT_PIN,INPUT);
  pinMode(ESC_PIN,OUTPUT);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);
  myESC.arm();
  delay(5000);
  digitalWrite(LED_BUILTIN,LOW);
  lcd.begin(16, 2);
  lcd.backlight();
  
  // Write to the LCD
  lcd.print("Drone Lejoola");
 
  // Wait for 5 seconds
  delay(5000);
 
  // Clear the LCD
  lcd.clear();
  for (int i=0;i=350;i++){
     myESC.speed(MIN_SPEED-200+i);
     delay(100);
  }
}
 
void loop() {
  
  lcd.home();
  lcd.print(millis());
  val=analogRead(POT_PIN);
  Serial.println(val);
  val=map(val,4095,MIN_SPEED ,MAX_SPEED);
  myESC.speed(val);
  delay(10);
  
  
  
}
