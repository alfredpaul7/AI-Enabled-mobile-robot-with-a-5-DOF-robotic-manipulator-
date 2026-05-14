#include <SPI.h>
#include <RF24.h>
#include <Servo.h>
#include <Wire.h>

RF24 radio(9,10);

const byte address[6]="00001";


struct ControlPacket
{
  int joyX;
  int joyY;

  bool joyBtn;

  bool b1;
  bool b2;
  bool b3;
  bool b4;
};


ControlPacket packet;


Servo s1,s2,s3,s4,s5;


int servo1=90;
int servo2=90;
int servo3=90;
int servo4=90;
int servo5=90;


volatile long encoder1=0;
volatile long encoder2=0;



#define MQ2_PIN A0
#define MQ7_PIN A1
#define MQ135_PIN A2
#define SMOKE_PIN A3
#define FIRE_PIN A6



unsigned long sensorTimer=0;



void encoderISR1()
{
  encoder1++;
}


void encoderISR2()
{
  encoder2++;
}



void setup()
{
  Serial.begin(115200);


  radio.begin();

  radio.openReadingPipe(0,address);

  radio.setPALevel(RF24_PA_LOW);

  radio.startListening();



  s1.attach(3);
  s2.attach(4);
  s3.attach(5);
  s4.attach(6);
  s5.attach(7);



  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);

  pinMode(13,OUTPUT);
  pinMode(A4,OUTPUT);



  attachInterrupt(
      digitalPinToInterrupt(2),
      encoderISR1,
      RISING
  );


  attachInterrupt(
      digitalPinToInterrupt(3),
      encoderISR2,
      RISING
  );


  Wire.begin();
}



void controlServos()
{
  if(packet.joyX>700) servo1++;
  if(packet.joyX<300) servo1--;

  if(packet.joyY>700) servo2++;
  if(packet.joyY<300) servo2--;


  if(packet.b1) servo3++;
  if(packet.b2) servo3--;

  if(packet.b3) servo4++;
  if(packet.b4) servo4--;


  if(packet.joyBtn)
    servo5=0;
  else
    servo5=90;


  servo1=constrain(servo1,0,180);
  servo2=constrain(servo2,0,180);
  servo3=constrain(servo3,0,180);
  servo4=constrain(servo4,0,180);



  s1.write(servo1);
  s2.write(servo2);
  s3.write(servo3);
  s4.write(servo4);
  s5.write(servo5);
}



void driveMotors()
{
  int speed=
      map(
          packet.joyY,
          0,
          1023,
          -255,
          255
      );


  if(speed>0)
  {
    digitalWrite(12,HIGH);
    analogWrite(11,speed);

    digitalWrite(A4,HIGH);
    analogWrite(13,speed);
  }
  else
  {
    digitalWrite(12,LOW);
    analogWrite(11,-speed);

    digitalWrite(A4,LOW);
    analogWrite(13,-speed);
  }
}



void sendSensorData()
{
  int mq2=analogRead(MQ2_PIN);

  int mq7=analogRead(MQ7_PIN);

  int mq135=analogRead(MQ135_PIN);

  int smoke=analogRead(SMOKE_PIN);

  int fire=analogRead(FIRE_PIN);



  Serial.print("{");


  Serial.print("\"mq2\":");
  Serial.print(mq2);

  Serial.print(",");


  Serial.print("\"mq7\":");
  Serial.print(mq7);

  Serial.print(",");


  Serial.print("\"mq135\":");
  Serial.print(mq135);

  Serial.print(",");


  Serial.print("\"smoke\":");
  Serial.print(smoke);

  Serial.print(",");


  Serial.print("\"fire\":");
  Serial.print(fire);

  Serial.print(",");


  Serial.print("\"enc1\":");
  Serial.print(encoder1);

  Serial.print(",");


  Serial.print("\"enc2\":");
  Serial.print(encoder2);

  Serial.print(",");


  Serial.print("\"s1\":");
  Serial.print(servo1);

  Serial.print(",");


  Serial.print("\"s2\":");
  Serial.print(servo2);


  Serial.println("}");
}



void loop()
{
  if(radio.available())
  {
    radio.read(
        &packet,
        sizeof(packet)
    );


    controlServos();

    driveMotors();
  }



  if(millis()-sensorTimer>200)
  {
    sensorTimer=millis();

    sendSensorData();
  }
}