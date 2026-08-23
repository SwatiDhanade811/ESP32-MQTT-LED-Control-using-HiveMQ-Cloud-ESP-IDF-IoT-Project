# ESP32 MQTT LED Control with HiveMQ Cloud

Remote control of an LED connected to ESP32 using MQTT protocol over a secure TLS connection to HiveMQ Cloud broker.

## Project Demo

![ESP32 MQTT LED Control](project_demo.png)

**Output Video:** [Watch on YouTube](https://youtu.be/OKMco-J3JLo?si=sgc1bR76ot9SNDn_)

## Overview

This project implements a publish-subscribe IoT architecture where:
- An **ESP32** microcontroller connects to Wi-Fi and subscribes to an MQTT topic
- A **HiveMQ Cloud** broker handles secure message routing (MQTTS, port 8883)
- Any **MQTT client** (HiveMQ Web Client, MQTT Explorer, mobile app, etc.) can publish `ON`/`OFF` commands to control the LED remotely

## Hardware Requirements

| Component | Details |
|-----------|---------|
| ESP32 DevKit | Any ESP32 development board |
| LED | External LED (connected to GPIO 4) |
| Resistor | 220 Ohm (current limiting) |
| Breadboard | For prototyping |
| Jumper Wires | Male-to-male |

### Circuit Diagram

```
ESP32 GPIO 4 ----> 220 Ohm Resistor ----> LED Anode (+)
                                          LED Cathode (-) ----> GND
```

## Software Stack

| Technology | Purpose |
|------------|---------|
| ESP-IDF (v5.x) | Espressif IoT Development Framework |
| FreeRTOS | Real-time task scheduling |
| MQTT over TLS | Secure communication protocol |
| HiveMQ Cloud | MQTT broker (free tier) |
| C Language | Firmware development |

## Features

- Secure MQTT communication over TLS (port 8883)
- Remote LED control from anywhere via internet
- Automatic Wi-Fi reconnection on disconnection
- Event-driven architecture using ESP-IDF event loop
- HiveMQ Cloud free tier compatible
- ESP-IDF certificate bundle for TLS verification (no manual cert management)
- Detailed logging via ESP_LOG

## Project Structure

```
MQTT_LED_HiveMQ/
├── CMakeLists.txt          # Project-level CMake configuration
├── sdkconfig               # ESP-IDF SDK configuration
├── main/
│   ├── CMakeLists.txt      # Component-level CMake (dependencies)
│   └── main.c             # Application source code
└── README.md
```

## Configuration

Edit the following macros in `main/main.c` before building:

```c
#define WIFI_SSID       "Your_WiFi_SSID"
#define WIFI_PASSWORD   "Your_WiFi_Password"

#define MQTT_BROKER_URI "mqtts://your-cluster.hivemq.cloud:8883"
#define MQTT_USERNAME   "your_mqtt_username"
#define MQTT_PASSWORD   "your_mqtt_password"

#define MQTT_TOPIC      "esp32/led"
#define LED_GPIO        GPIO_NUM_4
```

## HiveMQ Cloud Setup

1. Create a free account at [HiveMQ Cloud](https://www.hivemq.com/cloud/)
2. Create a new cluster (Serverless Free tier)
3. Add MQTT credentials (username/password) under Access Management
4. Note down the cluster URL (used as `MQTT_BROKER_URI`)

## Build & Flash

```bash
# Set up ESP-IDF environment
. ~/esp/esp-idf/export.sh

# Navigate to project directory
cd MQTT_LED_HiveMQ

# Build
idf.py build

# Flash (replace PORT with your serial port)
idf.py -p PORT flash

# Monitor serial output
idf.py -p PORT monitor
```

## Usage

1. Flash the firmware to ESP32
2. ESP32 connects to Wi-Fi and then to HiveMQ Cloud
3. Open [HiveMQ Web Client](http://www.hivemq.com/demos/websocket-client/) or any MQTT client
4. Connect to your HiveMQ cluster
5. Publish to topic `esp32/led`:
   - Send `ON` to turn LED on
   - Send `OFF` to turn LED off

## Serial Monitor Output

```
I (MQTT_LED): Starting MQTT LED project...
I (MQTT_LED): Connecting to Wi-Fi...
I (MQTT_LED): Got IP: 192.168.x.x
I (MQTT_LED): MQTT CONNECTED
I (MQTT_LED): Subscribed to topic: esp32/led
I (MQTT_LED): MQTT DATA RECEIVED
Topic: esp32/led
Data: ON
I (MQTT_LED): LED -> ON
```

## How It Works

1. **NVS Initialization** - Non-volatile storage for Wi-Fi credentials
2. **LED GPIO Setup** - Configure GPIO 4 as output, start with LED OFF
3. **Wi-Fi Connection** - STA mode with auto-reconnect
4. **MQTT TLS Connection** - Secure connection using ESP-IDF certificate bundle
5. **Topic Subscription** - Subscribe to `esp32/led` with QoS 1
6. **Message Handling** - Parse incoming data and toggle LED based on "ON"/"OFF"

## Topics Used

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `esp32/led` | Subscribe | Receive LED control commands |

## Dependencies (ESP-IDF Components)

- `mqtt` - MQTT client library
- `esp_wifi` - Wi-Fi driver
- `esp_event` - Event loop library
- `esp_netif` - Network interface
- `nvs_flash` - Non-volatile storage
- `esp-tls` - TLS support
- `driver` - GPIO driver

## License

This project is open source and available for educational purposes.

## Author

**Swati** - Embedded Systems / IoT Project
