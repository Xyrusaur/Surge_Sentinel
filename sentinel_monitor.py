import serial
import mysql.connector
from datetime import datetime, timedelta
import pytz
import paho.mqtt.client as mqtt
import uuid
import ssl
import time

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
dest_broker = "wsa.jackbord.org"
dest_port = 443  # Secure WSS port
dest_username = "117112657838025786605"
dest_password = "1b77bb526e"
dest_topic = "10Gy/cmd"
hi = 'hi'

# Define the callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.publish(dest_topic, hi)  # Publish 'hi' message on connection
    else:
        print(f"Connection failed with code {rc}")

# Define the callback function for disconnection
def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")

# Create an MQTT client instance
client_id = str(uuid.uuid4())
client = mqtt.Client(client_id, transport='websockets')

# Set username and password
client.username_pw_set(dest_username, dest_password)

# Assign the on_connect and on_disconnect callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Configure SSL/TLS
ssl_context = ssl.create_default_context()
client.tls_set_context(ssl_context)

# Connect to the broker using WSS
client.ws_set_options(path="/mqtt")
client.tls_insecure_set(True)  # if the server uses a self-signed certificate, use this line carefully

# Start the MQTT client loop
client.connect(dest_broker, dest_port)
client.loop_start()

# Initialize variables for averaging
average_window = []  # This will store pressure values for the last 5 seconds

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

                    # Add current pressure value to the average window
                    average_window.append((timestamp, water_pressure))

                    # Remove old values from the window (keep only last 5 seconds)
                    while average_window and (timestamp - average_window[0][0] > timedelta(seconds=5)):
                        average_window.pop(0)

                    # Calculate average pressure over last 5 seconds
                    if average_window:
                        avg_pressure = sum([item[1] for item in average_window]) / len(average_window)

                        # Publish MQTT message if average pressure exceeds 1100
                        if avg_pressure >= 1100:
                            client.publish(dest_topic, hi)
                            print(f'Published alert: Average pressure = {avg_pressure:.2f}')

                except ValueError:
                    print("Error: Invalid data format")

        # Delay to control the rate of readings (adjust as needed)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program")

# Close the database connection
cursor.close()
conn.close()

# Stop the MQTT client loop and disconnect
client.loop_stop()
client.disconnect()
