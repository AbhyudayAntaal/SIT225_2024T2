# smartphone_accelerometer_single_csv.py
import sys
import time
import traceback
import os
from arduino_iot_cloud import ArduinoCloudClient
import pandas as pd
from datetime import datetime

# Configuration
DEVICE_ID = "449b5450-27b4-4a65-91bd-da682e36d987"
SECRET_KEY = "m#7NknswtHHwtUTWk8BP?3mwo"
DATA_DIR = "accelerometer_data"
CSV_FILENAME = "all_accelerometer_data.csv"  # Single output file
MIN_INTERVAL = 0.02  # 20ms minimum between samples

class AccelerometerLogger:
    def __init__(self):
        self.data_buffer = []
        self.sample_count = 0
        self.last_sample_time = 0
        self.x = self.y = self.z = None
        self.client = None
        self.csv_initialized = False
        
    def on_x_changed(self, client, value):
        self.x = float(value) if value is not None else None

    def on_y_changed(self, client, value):
        self.y = float(value) if value is not None else None

    def on_z_changed(self, client, value):
        self.z = float(value) if value is not None else None

    def save_to_csv(self):
        """Append new samples to the single CSV file"""
        if not self.data_buffer:
            return
            
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        filepath = os.path.join(DATA_DIR, CSV_FILENAME)
        
        # Create DataFrame from new samples
        new_data = pd.DataFrame(self.data_buffer, 
                               columns=['Timestamp', 'X', 'Y', 'Z'])
        
        # Append to existing file or create new one
        if os.path.exists(filepath) and self.csv_initialized:
            new_data.to_csv(filepath, mode='a', header=False, index=False)
        else:
            new_data.to_csv(filepath, index=False)
            self.csv_initialized = True
            
        print(f"Added {len(self.data_buffer)} samples to {filepath}")
        self.data_buffer = []

    def collect_sample(self):
        current_time = time.time()
        
        if current_time - self.last_sample_time < MIN_INTERVAL:
            return False
            
        if all(v is not None for v in [self.x, self.y, self.z]):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            self.data_buffer.append([timestamp, self.x, self.y, self.z])
            self.sample_count += 1
            
            print(f"Sample {self.sample_count}: {timestamp} | "
                  f"X={self.x:.3f}, Y={self.y:.3f}, Z={self.z:.3f}")
            
            self.x = self.y = self.z = None
            self.last_sample_time = current_time
            
            # Save every 10 samples (can be adjusted)
            if len(self.data_buffer) >= 10:
                self.save_to_csv()
                
            return True
        return False

    def run(self):
        print("Initializing Arduino Cloud connection...")
        
        self.client = ArduinoCloudClient(
            device_id=DEVICE_ID,
            username=DEVICE_ID,
            password=SECRET_KEY,
            sync_mode=True
        )

        # Register variables - MUST match your Arduino Cloud exactly
        self.client.register("acc_x", value=None, on_write=self.on_x_changed)
        self.client.register("acc_y", value=None, on_write=self.on_y_changed)
        self.client.register("acc_z", value=None, on_write=self.on_z_changed)

        print(f"Starting data collection to {CSV_FILENAME}...")
        print("Press Ctrl+C to stop...")
        self.client.start()

        try:
            while True:
                self.client.update()
                self.collect_sample()
                time.sleep(0.001)
                
        except KeyboardInterrupt:
            print("\nStopping data collection...")
        except Exception as e:
            print(f"Error: {str(e)}")
            traceback.print_exc()
        finally:
            # Save any remaining data before exiting
            if self.data_buffer:
                self.save_to_csv()
            print(f"Collection stopped. Total samples collected: {self.sample_count}")
            print(f"All data saved to: {os.path.join(DATA_DIR, CSV_FILENAME)}")

if __name__ == "__main__":
    logger = AccelerometerLogger()
    try:
        logger.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)