static int relay_1 = 16; // D0
static int relay_2 = 5; // D1

static int time_on = 3000;
static int time_off = 500;

void setup() {
  pinMode(relay_1, OUTPUT);
  pinMode(relay_2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Relay 1: on  | off | off | off
  // Relay 1: off | off | on  | off
  
  digitalWrite(relay_1, LOW);
  digitalWrite(relay_2, HIGH);
  delay(time_on);
  
  digitalWrite(relay_1, HIGH);
  digitalWrite(relay_2, HIGH);
  delay(time_off);
  
  digitalWrite(relay_1, HIGH);
  digitalWrite(relay_2, LOW);
  delay(time_on);
  
  digitalWrite(relay_1, HIGH);
  digitalWrite(relay_2, HIGH);
  delay(time_off);
}
