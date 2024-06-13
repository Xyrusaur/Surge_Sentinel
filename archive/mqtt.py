import paho.mqtt.client as mqtt
import sys

# MQTT broker information
broker_address = "broker.hivemq.com"
port = 1883
username = "Surge_Sentinel"
password = "Surgesentinel1234"
topic = "alerts/wave-height"

# Callback function to handle connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

# Callback function to handle publishing
def on_publish(client, userdata, mid):
    print("Message published.")
    client.disconnect()
    sys.exit()

# Callback function to handle receiving messages
def on_message(client, userdata, msg):
    print("Received message: "+msg.payload.decode())

# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message  # Set the on_message callback

# Connect to MQTT broker
client.connect(broker_address, port)

# Publish message
message = "Hello, Surge Sentinel!"
client.publish(topic, message)