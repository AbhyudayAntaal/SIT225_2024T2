import serial
import time
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase with your credentials and database URL
cred = credentials.Certificate("C:/users/abhyu/downloads/firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://p-eeef9-default-rtdb.firebaseio.com/'
})

# Configure serial connection to use COM6
ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Allow time for the serial connection to initialize

# Reference in the Firebase DB where data will be stored
ref = db.reference('gyroscopeData')

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                # Expecting line format: "x,y,z"
                parts = line.split(',')
                if len(parts) == 3:
                    x, y, z = map(float, parts)
                    # Capture current timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # Prepare JSON payload
                    data_sample = {
                        "timestamp": timestamp,
                        "x": x,
                        "y": y,
                        "z": z
                    }
                    # Push data to Firebase
                    ref.push(data_sample)
                    print(f"Data pushed: {data_sample}")
            except ValueError as ve:
                print("Value error:", ve)
except KeyboardInterrupt:
    print("Data collection stopped.")
    ser.close()
