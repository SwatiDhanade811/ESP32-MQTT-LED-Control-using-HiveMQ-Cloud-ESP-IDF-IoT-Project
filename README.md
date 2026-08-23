# ESP32 MQTT LED Control using HiveMQ Cloud

This project demonstrates an IoT-based LED control system using an **ESP32, MQTT protocol, HiveMQ Cloud, and ESP-IDF**.

The ESP32 connects to a Wi-Fi network and establishes a secure MQTT connection with the HiveMQ Cloud broker. The device subscribes to the `esp32/led` MQTT topic and receives control commands remotely.

Based on the received MQTT message:
- `ON` → LED connected to GPIO 4 turns ON
- `OFF` → LED connected to GPIO 4 turns OFF

The project was developed using **C and ESP-IDF in Visual Studio Code** and includes GPIO configuration, Wi-Fi connectivity, MQTT client configuration, MQTT authentication, TLS communication, topic subscription, and event-based message handling.

### Hardware
- ESP32 Development Board
- LED
- Resistor
- Breadboard
- Jumper Wires

### Technologies
**ESP32 | C | ESP-IDF | MQTT | HiveMQ Cloud | Wi-Fi | TLS**

### Project Flow

ESP32 → Wi-Fi → HiveMQ Cloud MQTT Broker → MQTT Topic → ESP32 → GPIO 4 → LED

Output video: https://www.youtube.com/watch?v=OKMco-J3JLo

The attached demonstration video shows the successfully tested end-to-end MQTT communication and LED control.
