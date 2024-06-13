import serial
import mysql.connector
from datetime import datetime
import pytz
import paho.mqtt.client as mqtt
import uuid
import ssl
import json

# Serial port configuration
port = 'COM3'  # Replace with your actual serial port
baudrate = 115200  # Adjust baudrate if needed

# Open serial connection
ser = serial.Serial(port, baudrate)

# MySQL database configuration
db_config = {
    'user': 'surge_sentinel_admin',  # Replace with your MySQL username
    'password': 'Xyru$04147MS',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'sensor_data',
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Insert data into MySQL database
def insert_data(timestamp, water_pressure, water_depth):
    insert_query = (
        "INSERT INTO water_metrics (date_time, water_pressure, water_depth) "
        "VALUES (%s, %s, %s)"
    )
    data = (timestamp, water_pressure, water_depth)
    cursor.execute(insert_query, data)
    conn.commit()

# MQTT broker configuration
broker = '1291f6828b694b87a3aea196baa93933.s1.eu.hivemq.cloud'
port = 8883  # Secure MQTT port
username = 'sentinel'
password = 'Sentinel1234'
bootMessage = 'Hello, Surge Sentinel!'

# MQTT topics
alerts = 'sentinel/alerts'
boot = 'sentinel/boot'

# Define the callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.publish(boot, json.dumps({
            "message": bootMessage,
            "timestamp": datetime.now(pytz.timezone('Pacific/Auckland')).isoformat()
        }))
    else:
        print(f"Connection failed with code {rc}")

# Define the callback function for disconnection
def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")

# Create an MQTT client instance
client_id = str(uuid.uuid4())
client = mqtt.Client(client_id)

# Set username and password
client.username_pw_set(username, password)

# Assign the on_connect and on_disconnect callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Configure SSL/TLS
ssl_context = ssl.create_default_context()
client.tls_set_context(ssl_context)

# Connect to the broker
client.connect(broker, port)

# Start the MQTT client loop
client.loop_start()

# Function to publish an alert message if water pressure exceeds 1100
def publish_alert(water_pressure, water_depth, timestamp):
    alert_message = {
        "message": "Alert: High water pressure detected!",
        "water_pressure": water_pressure,
        "water_depth": water_depth,
        "timestamp": timestamp.isoformat()
    }
    client.publish(alerts, json.dumps(alert_message))
    print("Published alert message")

# Read data from serial monitor in a loop
try:
    while True:
        # Read incoming line
        data_line = ser.readline().decode('utf-8').strip()

        # Check if data is available
        if data_line:
            # Split data into list if needed (optional)
            data_list = data_line.split(',')

            # Get current timestamp with timezone information
            local_tz = pytz.timezone('Pacific/Auckland')
            timestamp = datetime.now(local_tz)

            # Ensure the data list has the correct number of elements
            if len(data_list) == 2:
                try:
                    water_pressure = float(data_list[0])
                    water_depth = float(data_list[1])

                    # Insert data into MySQL database
                    insert_data(timestamp, water_pressure, water_depth)

                    # Publish MQTT message if water pressure exceeds 1100
                    if water_pressure > 1100:
                        publish_alert(water_pressure, water_depth, timestamp)
                except ValueError:
                    print("Error: Invalid data format")
except KeyboardInterrupt:
    print("Exiting program")

# Close the database connection
cursor.close()
conn.close()

# Stop the MQTT client loop and disconnect
client.loop_stop()
client.disconnect()
