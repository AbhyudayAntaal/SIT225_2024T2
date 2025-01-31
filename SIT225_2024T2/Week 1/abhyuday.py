import serial
import time
from datetime import datetime
import random

arduino_port = "COM6"  
baud_rate = 9600

try:
    conn = serial.Serial(arduino_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def log_event(event):
    """Logs events with timestamps."""
    print(f"{datetime.now()} | {event}")

try:
    while True:
        num_to_send = random.randint(1, 10)
        conn.write(f"{num_to_send}\n".encode())
        log_event(f"Sent to Arduino: {num_to_send}")

        arduino_response = conn.readline().decode("utf-8").strip()
        if arduino_response.isdigit():
            delay_seconds = int(arduino_response)
            log_event(f"Received from Arduino: {delay_seconds}")
            
            log_event(f"Sleeping for {delay_seconds} seconds...")
            time.sleep(delay_seconds)
            log_event("Sleep completed.")
        
except KeyboardInterrupt:
    log_event("Program interrupted by user.")
finally:
    conn.close()
