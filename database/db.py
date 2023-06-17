import paho.mqtt.client as mqtt
import sqlite3
from time import time


mqtt_broker = "mqtt.flespi.io"
mqtt_port = 1883
mqtt_username = 'FKyPwilNTQJsBhDscQN9IceJwA5AW56pEv20BbBiR8Bid2yfG9cfchMyFIYrBSE5'
mqtt_password = ''
mqtt_topic_temperature = "temperature"
mqtt_topic_humidity = "humidity"

sqlite_database = "temphum.db"
conn = sqlite3.connect(sqlite_database, check_same_thread=False)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                  (timestamp INTEGER, temperature REAL, humidity REAL)''')
conn.commit()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(mqtt_topic_temperature)
    client.subscribe(mqtt_topic_humidity)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    timestamp = int(time())

    if topic == mqtt_topic_temperature:
        temperature = float(payload)
        humidity = None
    elif topic == mqtt_topic_humidity:
        temperature = None
        humidity = float(payload)

    if temperature is not None or humidity is not None:
        # Insert data into the SQLite database
        cursor.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, temperature, humidity))
        conn.commit()

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Start the MQTT client loop
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    conn.close()
