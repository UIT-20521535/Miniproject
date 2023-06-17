from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt

broker_address = "mqtt.flespi.io"
broker_port = 8883
broker_username = "FKyPwilNTQJsBhDscQN9IceJwA5AW56pEv20BbBiR8Bid2yfG9cfchMyFIYrBSE5"
broker_password = ""
client = mqtt.Client(client_id="client_id")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("humidity")
    client.subscribe("temperature")


def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print("Received message:", payload, "from topic:", topic)
    if topic == "temperature":
        app.config['TEMPERATURE'] = payload
    elif topic == "humidity":
        app.config['HUMIDITY'] = payload


client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(broker_username, broker_password)
client.tls_set()

client.connect(broker_address, broker_port, keepalive=60)

client.loop_start()


app = Flask(__name__)

app.config['TEMPERATURE'] = ''
app.config['HUMIDITY'] = ''


@app.route('/get_data', methods=['GET'])
def get_data():
    global temperature, humidity
    return jsonify({'temperature': app.config['TEMPERATURE'], 'humidity': app.config['HUMIDITY']})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
