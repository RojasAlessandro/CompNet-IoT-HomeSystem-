import board
import adafruit_dht
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json

# --- GPIO Setup ---
LED_PIN = 17  # GPIO17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# --- DHT11 Setup ---
dht = adafruit_dht.DHT11(board.D4)

# --- MQTT Setup ---
BROKER = "192.168.218.35"
DHT_TOPIC = "iot/dht11/status"
LED_CONTROL_TOPIC = "iot/led_b/control"
LED_STATUS_TOPIC = "iot/led_b/status"

client = mqtt.Client()

# --- Global LED Control Variable ---
led_on = False

# --- MQTT Handlers ---
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)
    client.subscribe(LED_CONTROL_TOPIC)

def on_message(client, userdata, msg):
    global led_on
    payload = msg.payload.decode().lower()
    print(f"Received on {msg.topic}: {payload}")
    if msg.topic == LED_CONTROL_TOPIC:
        if payload == "on":
            GPIO.output(LED_PIN, GPIO.HIGH)
            client.publish(LED_STATUS_TOPIC, "ON")
            print("LED turned ON via MQTT")
            led_on = True
        elif payload == "off":
            GPIO.output(LED_PIN, GPIO.LOW)
            client.publish(LED_STATUS_TOPIC, "OFF")
            print("LED turned OFF via MQTT")
            led_on = False

# --- MQTT Setup ---
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()

# --- Main Loop ---
try:
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity

            if temperature is not None and humidity is not None:
                payload = {
                    "temperature": temperature,
                    "humidity": humidity
                }
                client.publish(DHT_TOPIC, json.dumps(payload))
                print(f"Published: {payload}")
                rounded_temp = round(temperature, 1)

                # --- Temperature-based LED auto control ---
                if rounded_temp <= 24 and not led_on:
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    client.publish(LED_STATUS_TOPIC, "ON")
                    print("Temp <= 24°C → LED turned ON")
                    led_on = True
                elif rounded_temp > 24 and led_on:
                    GPIO.output(LED_PIN, GPIO.LOW)
                    client.publish(LED_STATUS_TOPIC, "OFF")
                    print("Temp > 24°C → LED turned OFF")
                    led_on = False

            else:
                print("Sensor returned None values.")

        except Exception as e:
            print("Error reading DHT11:", e)

        time.sleep(5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()