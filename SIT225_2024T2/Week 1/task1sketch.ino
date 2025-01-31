int val;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);  
  randomSeed(analogRead(0));
}

void loop() {
  if (Serial.available() > 0) {
    val = Serial.parseInt();
    Serial.print("Received: ");
    Serial.println(val);

    for (int i = 0; i < val; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000);
      digitalWrite(LED_BUILTIN, LOW);
      delay(1000);
    }

    int randomNumber = random(1, 10);
    Serial.println(randomNumber);
  }
}
