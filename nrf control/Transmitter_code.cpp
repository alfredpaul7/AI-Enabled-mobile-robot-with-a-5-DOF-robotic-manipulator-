#include <SPI.h>
#include <RF24.h>

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

void setup()
{
  pinMode(2,INPUT_PULLUP);

  pinMode(3,INPUT_PULLUP);
  pinMode(4,INPUT_PULLUP);
  pinMode(5,INPUT_PULLUP);
  pinMode(6,INPUT_PULLUP);

  Serial.begin(115200);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);

  radio.stopListening();
}

void loop()
{
  packet.joyX=analogRead(A0);
  packet.joyY=analogRead(A1);

  packet.joyBtn=!digitalRead(2);

  packet.b1=!digitalRead(3);
  packet.b2=!digitalRead(4);
  packet.b3=!digitalRead(5);
  packet.b4=!digitalRead(6);

  radio.write(&packet,sizeof(packet));

  delay(20);
}