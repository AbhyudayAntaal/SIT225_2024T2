#include "thingProperties.h"
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  initProperties();  // Initialize Cloud properties

  // Connect to Arduino Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  // Initialize the LSM6DS3 sensor
  if (!IMU.begin()) {
    Serial.println("Failed to initialize LSM6DS3!");
    while (1);
  }
}

void loop() {
  ArduinoCloud.update();  // Send data to Arduino Cloud

  // Read accelerometer data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accel_x, accel_y, accel_z);

    // Print values for debugging
    Serial.print(accel_x);
    Serial.print(", ");
   Serial.print(accel_y);
   Serial.print(", ");
     Serial.println(accel_z);
  }
  
  delay(1000);  // Delay 1 second
}