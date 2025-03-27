import firebase_admin
from firebase_admin import credentials, db
import random
import time

# Initialize Firebase Admin with your service account and database URL
cred = credentials.Certificate("C:/Users/abhyu/Downloads/activityweek5-firebase-adminsdk-fbsvc-f8bde6c723.json")  # Update with your JSON file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://activityweek5-default-rtdb.firebaseio.com'  # Replace with your Firebase DB URL
})

def generate_random_sr04_data():
    # Generate random distance in centimeters (SR04 sensor typically measures from 2cm to 400cm)
    distance = round(random.uniform(2.0, 400.0), 2)
    return {
        "distance": distance,
        "timestamp": int(time.time())
    }

# Reference node for SR04 sensor data
sensor_ref = db.reference('SR04_ultrasonic')

# Insert generated data into Firebase
data = generate_random_sr04_data()
new_entry = sensor_ref.push(data)
print("Inserted Data:", data)

# Query all data from the SR04_ultrasonic node
all_data = sensor_ref.get()
print("\nAll Data in Firebase:")
for key, entry in all_data.items():
    print(f"{key}: {entry}")
