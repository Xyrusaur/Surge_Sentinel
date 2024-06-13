import paho.mqtt.client as mqtt

# Define the details for the MQTT connection
broker = "wsa.jackbord.org"
port = 443
username = "101420912423480827669"
password = "15e0e16960"
topic = "10Hm/cmd"
websocket_path = "/mqtt"

# Define the callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic)
        # Publish the message upon successful connection
        client.publish(topic, "runu 1")
    else:
        print("Connect failed with code", rc)

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

# Create the MQTT client
client = mqtt.Client(transport="websockets")

# Set the WebSocket path
client.ws_set_options(path=websocket_path)

# Set the username and password
client.username_pw_set(username, password)

# Enable SSL/TLS
client.tls_set()

# Assign the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port)

# Loop forever
client.loop_forever

# Disconnect
# client.disconnect()