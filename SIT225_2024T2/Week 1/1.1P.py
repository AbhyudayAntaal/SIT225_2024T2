import serial
import time
from datetime import datetime
import random

arduino_port = "COM6"  
baud_rate = 9600

# Attempt to connect to Arduino via serial port
try:
    conn = serial.Serial(arduino_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Function to log messages with timestamps
def log_event(event):
    print(f"{datetime.now()} | {event}")

try:
    while True:
        # Generate and send a random number to Arduino
        num_to_send = random.randint(1, 10)
        conn.write(f"{num_to_send}\n".encode())
        log_event(f"Sent to Arduino: {num_to_send}")

        # Read response from Arduino
        arduino_response = conn.readline().decode("utf-8").strip()
        if arduino_response.isdigit():
            delay_seconds = int(arduino_response)
            log_event(f"Received from Arduino: {delay_seconds}")
            
            # Wait for the specified time
            log_event(f"Sleeping for {delay_seconds} seconds...")
            time.sleep(delay_seconds)
            log_event("Sleep completed.")

# Handle manual interruption (Ctrl+C)
except KeyboardInterrupt:
    log_event("Program interrupted by user.")
finally:
    # Always close the serial connection
    conn.close()
