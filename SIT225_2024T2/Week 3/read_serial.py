import serial
import csv
import time

# Replace 'COM3' with the appropriate port (e.g., '/dev/ttyACM0' on Linux/Mac)
ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Allow time for the serial connection to initialize

# Open a CSV file in write mode
with open('accelerometer_data.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header row
    csv_writer.writerow(['timestamp', 'accel_x', 'accel_y', 'accel_z'])
    
    try:
        while True:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Expecting data in the format: "accel_x, accel_y, accel_z"
                parts = line.split(',')
                if len(parts) == 3:
                    try:
                        # Convert the parts to floats
                        x = float(parts[0].strip())
                        y = float(parts[1].strip())
                        z = float(parts[2].strip())
                        # Get the current timestamp
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        # Write the row to CSV
                        csv_writer.writerow([timestamp, x, y, z])
                        print(f"{timestamp} - X: {x}, Y: {y}, Z: {z}")
                    except ValueError:
                        # Skip lines with invalid numeric data
                        continue
    except KeyboardInterrupt:
        print("Data logging stopped.")
    finally:
        ser.close()
