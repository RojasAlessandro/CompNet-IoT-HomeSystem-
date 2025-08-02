import RPi.GPIO as GPIO
import time
import json
import threading
import cv2
from flask import Flask, Response
import paho.mqtt.client as mqtt

# GPIO Pins
TOUCH_PIN = 17
SERVO_PIN = 18
LED_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TOUCH_PIN, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# Servo PWM setup
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
servo.start(0)

# MQTT Setup
BROKER = "192.168.198.35"  # Replace with your Pi A's IP
TOUCH_TOPIC = "iot/touch"
CONTROL_TOPIC = "iot/door/control"
LED_STATUS_TOPIC = "iot/led/status"

client = mqtt.Client()

def set_angle(angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received on {msg.topic}: {payload}")
    if msg.topic == CONTROL_TOPIC:
        if payload == "open":
            print("Opening door")
            set_angle(180)
        elif payload == "close":
            print("Closing door")
            set_angle(0)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)
    client.subscribe(CONTROL_TOPIC)

def setup_mqtt():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.subscribe(CONTROL_TOPIC)
    client.loop_start()

# Flask app for webcam
app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def start_flask():
    app.run(host='0.0.0.0', port=8000)

def main():
    setup_mqtt()

    # Start webcam stream in background
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    try:
        last_touched_time = 0
        led_on = False

        while True:
            touched = GPIO.input(TOUCH_PIN)

            if touched:
                if not led_on:
                    print("Touched - LED ON")
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    client.publish(TOUCH_TOPIC, json.dumps({"touched": True}))
                    client.publish(LED_STATUS_TOPIC, "ON")
                    led_on = True
                    last_touched_time = time.time()
            elif led_on and (time.time() - last_touched_time >= 5):
                print("LED OFF (5s timeout)")
                GPIO.output(LED_PIN, GPIO.LOW)
                client.publish(TOUCH_TOPIC, json.dumps({"touched": False}))
                client.publish(LED_STATUS_TOPIC, "OFF")
                led_on = False

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        servo.stop()
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()
        camera.release()

if __name__ == "__main__":
    main()
