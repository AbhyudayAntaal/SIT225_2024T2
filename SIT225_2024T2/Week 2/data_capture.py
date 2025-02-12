import os
import serial
import time
import csv
from datetime import datetime

directory = 'data'
csv_filename = os.path.join(directory, 'ultrasonic_data.csv')

if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Directory '{directory}' created.")

SERIAL_PORT = 'COM6'  
BAUD_RATE = 9600

def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return

    with open(csv_filename, mode='a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        if os.stat(csv_filename).st_size == 0:
            csv_writer.writerow(["timestamp", "distance_cm"])
        
        print("Starting data capture. Press Ctrl+C to stop.")
        try:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        try:
                            distance = float(line)
                            timestamp = get_timestamp()
                            csv_writer.writerow([timestamp, distance])
                            print(f"{timestamp}, {distance}")
                        except ValueError:
                            print(f"Received non-numeric data: {line}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Data collection stopped by user.")
        finally:
            ser.close()

if __name__ == '__main__':
    main()
