import paho.mqtt.client as mqtt
import uuid
import ssl
import time

broker = '1291f6828b694b87a3aea196baa93933.s1.eu.hivemq.cloud'
port = 8883  # Secure MQTT port
username = 'sentinel'
password = 'Sentinel1234'
topic = 'sentinel/alerts'
message = 'Hello, MQTT! 01'

# Define the callback function for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.publish(topic, message)
        print("Published message")
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

# Wait for a short period to ensure the message is sent
time.sleep(10)

# Stop the MQTT client loop and disconnect
client.loop_stop()
client.disconnect()