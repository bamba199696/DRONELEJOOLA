/*
 code projet drone nautique lejoola 
@author:khadim mbacke ndiaye 
@author:Sanoum Niang
*/
#include <Wire.h>
#include <LCD03.h>
#include <ESPServo.h>
#include "ESC.h"


#define ESC_PIN_G(33)
#define ESC_PIN_D(34)
#define ESC_PIN_H(35)
#define LED_BUILTIN(2)
#define POT_PIN(36)
#define MIN_SPEED 1040
#define MAX_SPEED 1240
ESC myESC_G(ESC_PIN_G,1000,2000,500);
ESC myESC_D(ESC_PIN_D,1000,2000,500);
ESC myESC_H(ESC_PIN_H,1000,2000,500);
long int val;
LCD03 lcd;
 
void setup() {
  serial.begin(9600);
  delay(1000);

  pinMode(POT_PIN,INPUT);
  pinMode(ESC_PIN_D,OUTPUT);
  pinMode(ESC_PIN_G,OUTPUT);
  pinMode(ESC_PIN_H,OUTPUT);
  pinMode(LED_BUILTIN,OUTPUT);
  
  digitalWrite(LED_BUILTIN,HIGH);
  
  myESC_G.arm();
  myESC_D.arm();
  myESC_H.arm();
  delay(5000);
  digitalWrite(LED_BUILTIN,LOW);
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.setCursor(0,1);
  
  // Write to the LCD
  lcd.print("Drone Lejoola");
 
  // Wait for 5 seconds
  delay(5000);
 
  // Clear the LCD
  lcd.clear();
  for (int i=0;i=350;i++){
     myESC_G.speed(MIN_SPEED-200+i);
     myESC_D.speed(MIN_SPEED-200+i);
     myESC_H.speed(MIN_SPEED-200+i);
     delay(100);
  }
}
 
void loop() {
  
  lcd.home();
  lcd.print(millis());
  // val=analogRead(POT_PIN);
  // Serial.println(val);
  // val=map(val,4095,MIN_SPEED ,MAX_SPEED);
  // myESC.speed(val);
  // delay(10);

  avancer();

  reculer();

  gauche();

  droite();
  
}

void avancer() {
  val=map(2000, 0, 4095 , MIN_SPEED, MAX_SPEED);
  myESC_G.speed(val);
  myESC_D.speed(val);
  delay(10000);
}

void reculer() {
  val=map(-2000, -4095, 0, MIN_SPEED, MAX_SPEED);
  myESC_G.speed(val);
  myESC_D.speed(val);
  delay(10000);
}

void gauche() {
  val=map(2000, 0, 4095, MIN_SPEED, MAX_SPEED);
  myESC_G.speed(0);
  myESC_D.speed(val);
  delay(10000);
}

void droite() {
  val=map(2000, 0, 4095, MIN_SPEED, MAX_SPEED);
  myESC_G.speed(val);
  myESC_D.speed(0);
  delay(10000);
}
