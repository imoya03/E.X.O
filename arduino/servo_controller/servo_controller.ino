#include <Servo.h>

Servo servo1; // Servo objects
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;

int angleValues[6]; // Array of angle values
int servoPins[] = { 3, 4, 5, 6, 9, 10, 11 }; // Pins of servos

/*
Pin 3 = Root
Pin 4 = Arm A1
Pin 5 = Arm A2
Pin 6 = Wrist B
Pin 9 = Wrist A
Pin 10 = Arm B
Pin 11 = Gripper
*/

void setup()
{
  Serial.begin(9600); // Start serial communication

  // Setting pin mode of servo pins
  for (int i = 0; i < 7; i++)
  {
    pinMode(servoPins[i], OUTPUT);
  }

  // Servo nesnelerini bağla
  servo1.attach(servoPins[0]);
  servo2.attach(servoPins[1]);
  servo3.attach(servoPins[2]);
  servo4.attach(servoPins[3]);
  servo5.attach(servoPins[4]);
  servo6.attach(servoPins[5]);
  servo7.attach(servoPins[6]);
  digitalWrite(13,LOW);
}

void loop()
{
  if (Serial.available() >= 6) // If recieve data from serial port at least 6 bytes
  {
    // Read the angle values
    for (int i = 0; i < 6; i++)
    {
      angleValues[i] = Serial.parseInt(); // Read next int data


    }

    // Move the servos
    servo1.write(angleValues[0]); // Root
    servo2.write(angleValues[1]); // Arm A1
    servo3.write(180 - angleValues[1]); // Arm A2
    servo4.write(angleValues[2]); // Wrist B
    servo5.write(angleValues[3]); // Wrist A
    servo6.write(angleValues[4]); // Arm B
    servo7.write(angleValues[5]); // Gripper

  }
}