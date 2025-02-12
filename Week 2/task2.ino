const int trigPin = 9;  
const int echoPin = 2; 

void setup() {
  Serial.begin(9600);       
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  
  float distance = (duration * 0.0343) / 2;
  
  Serial.println(distance, 2);
  
  delay(1000);
}
