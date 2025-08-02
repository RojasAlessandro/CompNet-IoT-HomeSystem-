# 🏠 Smart Home IoT Network Simulation (INF1006 Project)

This project simulates a smart home IoT system using three interconnected Raspberry Pis. It showcases real-time sensing, remote control, and device communication using lightweight protocols like MQTT and HTTP.

## 🌐 Overview

We simulate three key smart home functionalities:

- **Thermostat-controlled LED light**
- **Touch-based doorbell with servo-controlled door**
- **Live camera feed acting as a digital peephole**
- **Centralized ReactJS web dashboard with real-time status updates**

## 🖥️ System Architecture

- **Pi A** - 🖧 *Web Server + MQTT Broker*  
  - Hosts the ReactJS dashboard (Flask backend)
  - MQTT broker using Mosquitto
  - Receives sensor data and sends control messages

- **Pi B** - 🌡️ *Thermostat + LED Controller*  
  - Monitors temperature & humidity using DHT11
  - Automatically toggles an LED light based on thresholds (simulating day/night)
  - Publishes data/status to Pi A via MQTT

- **Pi C** - 🚪 *Door Controller + Camera Feed*  
  - Detects touch (simulating a doorbell)
  - Activates a door LED and streams a live webcam feed via Flask
  - Receives commands from the web dashboard to open/close a servo-controlled door

## 📡 Communication Protocols

| Protocol | Purpose |
|---------|---------|
| MQTT    | Publish-subscribe messaging between devices |
| HTTP    | Web interface delivery & live video stream (Flask) |

## 📷 Live Webcam Feed

- Hosted from **Pi C** via Flask at:

http://<PI_C_IP>:8000/video_feed
(Embedded into the web dashboard hosted by **Pi A**)

## 🧠 Features

- 🔄 Real-time LED status, temperature, and door status
- 📷 Remote viewing of front-door webcam
- 🔐 Open/close door via website
- 🌡️ Automatic lighting based on temperature
- 📶 All devices connected over a mobile hotspot (SSID: SmartHome_IoT)


## 📂 Files & Responsibilities

| File                          | Purpose                                                  |
|-------------------------------|----------------------------------------------------------|
| `web_server_v3.py`           | Flask server for MQTT backend and legacy HTML UI        |
| `index.html`                 | Old dashboard interface (superseded by React)            |
| `iot_dht11_controller.py`    | Pi B controller: reads DHT11 sensor + toggles LED        |
| `iot_door_controller_v3.py`  | Pi C controller: handles touch sensor, webcam, servo, LED|
| `compnet-app/`               | ReactJS dashboard frontend (Node + TailwindCSS)          |
| `assets/CompNet Project.mp4` | Demo video of the working system                         |
| `assets/INF1006 Team Project Poster.pdf` | Project poster (for showcase/documentation)      |

📚 Technologies Used
Raspberry Pi (Python 3)

Flask

Paho MQTT

ReactJS + Tailwind CSS

DHT11, Touch Sensor, LED, Servo, Webcam (USB)

## 🚀 How to Run

1. Clone the repo to all 3 Pis.
2. Install dependencies (`Flask`, `paho-mqtt`, `RPi.GPIO`, `cv2`, etc.).
3. Start the Mosquitto broker on Pi A.
4. Run `web_server_v3.py` on Pi A.
5. Run `iot_dht11_controller.py` on Pi B.
6. Run `iot_door_controller_v3.py` on Pi C.
7. Access the dashboard via `http://<PI_A_IP>:5050`.

## 👨‍💻 Contributors

- **Andre Rojas** - System Integrator & Pi C (Webcam + Servo) Developer
- Ang Ke Ying, Choh Kaifeng, Raffael Harjanto, Tay Yu Xuan Jolene

> Built as part of SIT's Computer Networks Module (INF1006)

How to Run:
On Pi A (MQTT + Webserver)
sudo systemctl mosquitto
sudo python3 web_server_v3.py

On Pi B (Sensor Controller)
sudo python3 iot_dht11_controller.py

On Pi C (Door Controller + Webcam)
python3 iot_door_controller_v3.py

ReactJS Dashboard
cd compnet-app
npm install
npm start

🔒 Notes
All Raspberry Pis must connect to same network (e.g., mobile hotspot/router)

Adjust the MQTT broker_address in scripts to match Pi A’s IP (e.g., 192.168.218.61)

Firewall may block Flask ports (5050, 8000); allow them for visibility as well as PC or Laptops may be
blocking the Pi's from connecting to Putty if you do not have a monitor with you to get inside it.

Please double check the IP addresses of the Pi's via mobile hotspot in your phone and it is recommended to non apple
phones if possible




