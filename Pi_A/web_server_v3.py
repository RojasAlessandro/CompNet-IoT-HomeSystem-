from flask import Flask, render_template, request
import paho.mqtt.client as mqtt

app = Flask(__name__)
led_status = "OFF"  # Default status

# MQTT setup
MQTT_BROKER = "localhost"
TOUCH_TOPIC = "iot/touch"
CONTROL_TOPIC = "iot/door/control"
DHT_TOPIC = "iot/dht"
temperature = None
humidity = None

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)
    client.subscribe(TOUCH_TOPIC)
    client.subscribe(DHT_TOPIC)


def on_message(client, userdata, msg):
    global led_status, temperature, humidity
    payload = msg.payload.decode()
    print(f"Received on {msg.topic}: {payload}")
    if msg.topic == TOUCH_TOPIC:
        if "true" in payload.lower():
            led_status = "ON"
        else:
            led_status = "OFF"
    elif msg.topic == DHT_TOPIC:
        try:
            import json
            data = json.loads(payload)
            temperature = data.get("temperature")
            humidity = data.get("humidity")
        except Exception as e:
            print("Failed to parse DHT payload:", e)

# MQTT client setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("servo")
        if action == "open":
            mqtt_client.publish(CONTROL_TOPIC, "open")
        elif action == "close":
            mqtt_client.publish(CONTROL_TOPIC, "close")
    return render_template("index.html", led_status=led_status, temperature=temperature, humidity=humidity)

@app.route("/led_status", methods=["GET"])
def get_led_status():
    return {"status": led_status}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)














 led_status}