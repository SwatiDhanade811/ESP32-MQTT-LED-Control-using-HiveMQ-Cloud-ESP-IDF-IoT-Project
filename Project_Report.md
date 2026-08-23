# MQTT LED Control using ESP32 & HiveMQ Cloud

## Project Report

---

## 1. Project Overview

This project demonstrates **IoT-based LED control** using an ESP32 microcontroller connected to the **HiveMQ Cloud MQTT broker**. The system allows remote ON/OFF control of an external LED via MQTT messages sent from any MQTT client (e.g., HiveMQ Web Client).

---

## 2. Hardware Setup

![ESP32 LED Control Setup](ESP32_LED_Control_output.mp4)

**Hardware Used:**
| Component | Description |
|-----------|-------------|
| ESP32 DevKit | Main microcontroller (Wi-Fi enabled) |
| External LED (Blue) | Connected to GPIO 4 |
| Resistor (220Ω) | Current limiting resistor for LED |
| Breadboard | For circuit connections |
| Jumper Wires | For wiring components |

**Circuit Connections:**
- GPIO 4 → Resistor (220Ω) → LED Anode (+)
- LED Cathode (-) → GND

---

## 3. Project Demo

![ESP32 MQTT LED Control - Working Demo](project_demo.png)

> The image shows the complete working setup: ESP32 on a breadboard with a blue LED glowing, the ESP-IDF terminal showing MQTT messages being received, and the HiveMQ Web Client on the right laptop used to publish ON/OFF commands.

---

## 4. Software Architecture

```
┌─────────────────┐         ┌──────────────────────┐         ┌─────────────┐
│  MQTT Client    │──MQTT──▶│  HiveMQ Cloud Broker │──MQTT──▶│   ESP32     │
│ (Web/App/CLI)   │  (TLS)  │  (mqtts:// port 8883)│  (TLS)  │  (GPIO 4)  │
│                 │         │                      │         │   → LED     │
└─────────────────┘         └──────────────────────┘         └─────────────┘
```

**Communication Flow:**
1. ESP32 connects to Wi-Fi
2. ESP32 establishes secure MQTT connection (TLS) to HiveMQ Cloud
3. ESP32 subscribes to topic: `esp32/led`
4. User publishes "ON" or "OFF" to `esp32/led` from any MQTT client
5. ESP32 receives the message and toggles LED accordingly

---

## 5. Key Configuration

| Parameter | Value |
|-----------|-------|
| **Wi-Fi SSID** | Swati_Hotspot |
| **MQTT Broker** | HiveMQ Cloud (TLS, port 8883) |
| **MQTT Topic** | `esp32/led` |
| **LED GPIO Pin** | GPIO 4 |
| **Security** | TLS with ESP-IDF certificate bundle |
| **QoS Level** | 1 (At least once delivery) |

---

## 6. Software Components

### 6.1 Modules Used

| Module | Purpose |
|--------|---------|
| `esp_wifi` | Wi-Fi STA mode connection |
| `mqtt_client` | MQTT client (publish/subscribe) |
| `esp_crt_bundle` | TLS certificate verification |
| `driver/gpio` | GPIO control for LED |
| `nvs_flash` | Non-volatile storage initialization |
| `freertos` | Task scheduling |

### 6.2 Code Structure

```
MQTT_LED_HiveMQ/
├── CMakeLists.txt          # Project-level build config
├── main/
│   ├── CMakeLists.txt      # Component-level build config
│   └── main.c             # Application source code
├── sdkconfig               # ESP-IDF configuration
└── README.md
```

---

## 7. Functional Description

### LED Initialization
- GPIO 4 configured as output with no pull-up/pull-down
- LED starts in OFF state

### Wi-Fi Connection
- Connects as STA (Station) mode
- Auto-reconnects on disconnection
- Logs IP address upon successful connection

### MQTT Communication
- Connects to HiveMQ Cloud using **MQTTS** (port 8883)
- Uses username/password authentication
- TLS secured via ESP-IDF's trusted certificate bundle
- Subscribes to `esp32/led` with QoS 1

### LED Control Logic
| Message Received | Action |
|-----------------|--------|
| `ON` | LED turns ON (GPIO HIGH) |
| `OFF` | LED turns OFF (GPIO LOW) |
| Other | Warning log: "Unknown command" |

---

## 8. Build & Flash Instructions

```bash
# Set ESP-IDF environment
. ~/esp/esp-idf/export.sh

# Build the project
idf.py build

# Flash to ESP32
idf.py -p /dev/ttyUSB0 flash

# Monitor serial output
idf.py -p /dev/ttyUSB0 monitor
```

---

## 9. Serial Monitor Output (from Demo)

```
I (MQTT_LED): MQTT CONNECTED
I (MQTT_LED): Subscribed to topic: esp32/led
I (MQTT_LED): MQTT SUBSCRIBED, msg_id=20325
I (MQTT_LED): MQTT DATA RECEIVED
Topic: esp32/led
Data: ON
I (MQTT_LED): LED -> ON
I (MQTT_LED): MQTT DATA RECEIVED
Topic: esp32/led
Data: OFF
I (MQTT_LED): LED -> OFF
```

---

## 10. Tools & Technologies

| Tool/Technology | Version/Details |
|----------------|-----------------|
| **ESP-IDF** | v5.x (Espressif IoT Development Framework) |
| **Microcontroller** | ESP32 DevKit |
| **MQTT Broker** | HiveMQ Cloud (Free Tier) |
| **Protocol** | MQTT over TLS (MQTTS) |
| **IDE** | VS Code with ESP-IDF Extension |
| **Language** | C |
| **RTOS** | FreeRTOS |

---

## 11. Features

- ✅ Secure MQTT communication over TLS
- ✅ Remote LED control from anywhere via internet
- ✅ Auto Wi-Fi reconnection on disconnection
- ✅ Clean event-driven architecture
- ✅ HiveMQ Cloud free tier compatible
- ✅ Minimal build configuration for fast compilation

---

## 12. Conclusion

This project successfully demonstrates IoT-based remote control of a hardware peripheral (LED) using the MQTT protocol with cloud connectivity. The ESP32 securely connects to HiveMQ Cloud and responds to real-time commands, showcasing a practical IoT publish-subscribe pattern that can be extended to control motors, relays, sensors, and other actuators.

---

**Author:** Swati  
**Platform:** ESP32 + ESP-IDF  
**Broker:** HiveMQ Cloud  
