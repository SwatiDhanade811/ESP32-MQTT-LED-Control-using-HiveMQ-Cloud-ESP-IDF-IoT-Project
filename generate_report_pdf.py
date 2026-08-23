"""
Generate PDF Report for MQTT LED HiveMQ Project
"""

from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, 'MQTT LED Control - ESP32 & HiveMQ Cloud', align='C')
        self.ln(7)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 51, 102)
        self.ln(2)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def bullet_point(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.cell(0, 5, '   - ' + text, new_x="LMARGIN", new_y="NEXT")

    def table_row(self, col1, col2, bold=False):
        style = 'B' if bold else ''
        self.set_font('Helvetica', style, 9)
        if bold:
            self.set_fill_color(0, 51, 102)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(240, 245, 255)
            self.set_text_color(30, 30, 30)
        self.cell(60, 7, col1, border=1, fill=True)
        self.cell(0, 7, col2, border=1, fill=not bold, new_x="LMARGIN", new_y="NEXT")

    def code_block(self, text):
        self.set_font('Courier', '', 8)
        self.set_text_color(0, 80, 0)
        self.set_fill_color(245, 245, 245)
        for line in text.split('\n'):
            self.cell(5)
            self.cell(0, 4, line, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def generate_report():
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Title Page ---
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font('Helvetica', 'B', 26)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, 'MQTT LED Control', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, 'Using ESP32 & HiveMQ Cloud', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)

    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, 'IoT Project Report', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, 'Embedded Systems', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, 'Author: Swati', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'Platform: ESP32 + ESP-IDF | Broker: HiveMQ Cloud', align='C', new_x="LMARGIN", new_y="NEXT")

    # --- Project Overview ---
    pdf.section_title('1. Project Overview')
    pdf.body_text(
        'This project demonstrates IoT-based LED control using an ESP32 microcontroller '
        'connected to the HiveMQ Cloud MQTT broker. The system allows remote ON/OFF control '
        'of an external LED via MQTT messages sent from any MQTT client (e.g., HiveMQ Web Client).'
    )
    pdf.body_text(
        'The ESP32 connects to Wi-Fi, establishes a secure TLS connection to HiveMQ Cloud, '
        'subscribes to the topic "esp32/led", and toggles an LED on GPIO 4 based on received messages.'
    )

    # --- Project Demo Image ---
    pdf.section_title('2. Project Demo & Output')

    # Try to find and embed the image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, 'project_demo.png')
    parent_img = os.path.join(os.path.dirname(script_dir), 'project_demo.png')

    if os.path.exists(img_path):
        pdf.image(img_path, x=15, w=180)
        pdf.ln(3)
    elif os.path.exists(parent_img):
        pdf.image(parent_img, x=15, w=180)
        pdf.ln(3)
    else:
        img_jpg = os.path.join(script_dir, 'project_demo.jpg')
        parent_jpg = os.path.join(os.path.dirname(script_dir), 'project_demo.jpg')
        if os.path.exists(img_jpg):
            pdf.image(img_jpg, x=15, w=180)
            pdf.ln(3)
        elif os.path.exists(parent_jpg):
            pdf.image(parent_jpg, x=15, w=180)
            pdf.ln(3)
        else:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(150, 0, 0)
            pdf.cell(0, 6, '[Image: project_demo.png not found - place it in the project folder]', new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 4,
        'Figure: Working setup showing ESP32 on breadboard with blue LED, ESP-IDF terminal '
        'displaying MQTT messages, and HiveMQ Web Client used to publish ON/OFF commands.')
    pdf.ln(2)

    # --- Output Video Link ---
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, 'Project Output Video:', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 200)
    pdf.cell(0, 5, 'https://youtu.be/OKMco-J3JLo?si=sgc1bR76ot9SNDn_', new_x="LMARGIN", new_y="NEXT", link='https://youtu.be/OKMco-J3JLo?si=sgc1bR76ot9SNDn_')
    pdf.ln(2)

    # --- Hardware Setup ---
    pdf.section_title('3. Hardware Setup')
    pdf.table_row('Component', 'Description', bold=True)
    pdf.table_row('ESP32 DevKit', 'Main microcontroller (Wi-Fi enabled)')
    pdf.table_row('External LED (Blue)', 'Connected to GPIO 4')
    pdf.table_row('Resistor (220 Ohm)', 'Current limiting resistor for LED')
    pdf.table_row('Breadboard', 'For circuit connections')
    pdf.table_row('Jumper Wires', 'For wiring components')
    pdf.ln(2)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 6, 'Circuit Connections:', new_x="LMARGIN", new_y="NEXT")
    pdf.bullet_point('GPIO 4 -> Resistor (220 Ohm) -> LED Anode (+)')
    pdf.bullet_point('LED Cathode (-) -> GND')

    # --- Software Architecture ---
    pdf.section_title('4. Software Architecture')
    pdf.body_text('Communication Flow:')
    pdf.code_block(
        '  +----------------+       +---------------------+       +-----------+\n'
        '  |  MQTT Client   |--TLS->| HiveMQ Cloud Broker |--TLS->|   ESP32   |\n'
        '  | (Web/App/CLI)  |       |  (port 8883)        |       |  (GPIO 4) |\n'
        '  +----------------+       +---------------------+       +-----+-----+\n'
        '                                                               |\n'
        '                                                              LED'
    )
    pdf.ln(1)
    pdf.body_text('Step-by-step flow:')
    pdf.bullet_point('1. ESP32 connects to Wi-Fi network')
    pdf.bullet_point('2. Establishes secure MQTT connection (TLS) to HiveMQ Cloud')
    pdf.bullet_point('3. Subscribes to topic: esp32/led')
    pdf.bullet_point('4. User publishes "ON" or "OFF" from any MQTT client')
    pdf.bullet_point('5. ESP32 receives message and toggles LED accordingly')

    # --- Configuration ---
    pdf.section_title('5. Key Configuration')
    pdf.table_row('Parameter', 'Value', bold=True)
    pdf.table_row('Wi-Fi SSID', 'Swati_Hotspot')
    pdf.table_row('MQTT Broker', 'HiveMQ Cloud (TLS, port 8883)')
    pdf.table_row('MQTT Topic', 'esp32/led')
    pdf.table_row('LED GPIO Pin', 'GPIO 4')
    pdf.table_row('Security', 'TLS with ESP-IDF certificate bundle')
    pdf.table_row('QoS Level', '1 (At least once delivery)')
    pdf.table_row('Authentication', 'Username/Password')

    # --- Software Components ---
    pdf.section_title('6. Software Components')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'ESP-IDF Modules Used:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.table_row('Module', 'Purpose', bold=True)
    pdf.table_row('esp_wifi', 'Wi-Fi STA mode connection')
    pdf.table_row('mqtt_client', 'MQTT client (publish/subscribe)')
    pdf.table_row('esp_crt_bundle', 'TLS certificate verification')
    pdf.table_row('driver/gpio', 'GPIO control for LED')
    pdf.table_row('nvs_flash', 'Non-volatile storage initialization')
    pdf.table_row('freertos', 'Task scheduling and delays')
    pdf.ln(2)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Project Structure:', new_x="LMARGIN", new_y="NEXT")
    pdf.code_block(
        'MQTT_LED_HiveMQ/\n'
        '|-- CMakeLists.txt       (Project-level build config)\n'
        '|-- sdkconfig            (ESP-IDF configuration)\n'
        '|-- main/\n'
        '|   |-- CMakeLists.txt   (Component build config)\n'
        '|   +-- main.c           (Application source code)\n'
        '+-- README.md'
    )

    # --- Functional Description ---
    pdf.section_title('7. Functional Description')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, 'LED Initialization:', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.bullet_point('GPIO 4 configured as output (no pull-up/pull-down)')
    pdf.bullet_point('LED starts in OFF state')
    pdf.ln(1)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, 'Wi-Fi Connection:', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.bullet_point('Connects in STA (Station) mode')
    pdf.bullet_point('Auto-reconnects on disconnection')
    pdf.bullet_point('Logs IP address upon successful connection')
    pdf.ln(1)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, 'MQTT Communication:', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.bullet_point('Connects to HiveMQ Cloud using MQTTS (port 8883)')
    pdf.bullet_point('Username/password authentication')
    pdf.bullet_point('TLS secured via ESP-IDF trusted certificate bundle')
    pdf.bullet_point('Subscribes to "esp32/led" with QoS 1')
    pdf.ln(1)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, 'LED Control Logic:', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.table_row('Message', 'Action', bold=True)
    pdf.table_row('ON', 'LED turns ON (GPIO HIGH)')
    pdf.table_row('OFF', 'LED turns OFF (GPIO LOW)')
    pdf.table_row('Other', 'Warning: "Unknown command"')

    # --- Serial Output ---
    pdf.section_title('8. Serial Monitor Output')
    pdf.body_text('Sample output from ESP-IDF monitor during operation:')
    pdf.code_block(
        'I (MQTT_LED): Starting MQTT LED project...\n'
        'I (MQTT_LED): Connecting to Wi-Fi...\n'
        'I (MQTT_LED): Wi-Fi started\n'
        'I (MQTT_LED): Got IP: 192.168.x.x\n'
        'I (MQTT_LED): Starting MQTT...\n'
        'I (MQTT_LED): MQTT client started\n'
        'I (MQTT_LED): MQTT CONNECTED\n'
        'I (MQTT_LED): Subscribed to topic: esp32/led\n'
        'I (MQTT_LED): MQTT SUBSCRIBED, msg_id=20325\n'
        'I (MQTT_LED): MQTT DATA RECEIVED\n'
        'Topic: esp32/led\n'
        'Data: ON\n'
        'I (MQTT_LED): LED -> ON\n'
        'I (MQTT_LED): MQTT DATA RECEIVED\n'
        'Topic: esp32/led\n'
        'Data: OFF\n'
        'I (MQTT_LED): LED -> OFF'
    )

    # --- Build Instructions ---
    pdf.section_title('9. Build & Flash Instructions')
    pdf.code_block(
        '# Set ESP-IDF environment\n'
        '. ~/esp/esp-idf/export.sh\n'
        '\n'
        '# Build the project\n'
        'idf.py build\n'
        '\n'
        '# Flash to ESP32\n'
        'idf.py -p /dev/ttyUSB0 flash\n'
        '\n'
        '# Monitor serial output\n'
        'idf.py -p /dev/ttyUSB0 monitor'
    )

    # --- Tools & Technologies ---
    pdf.section_title('10. Tools & Technologies')
    pdf.table_row('Tool / Technology', 'Details', bold=True)
    pdf.table_row('ESP-IDF', 'v5.x (Espressif IoT Dev Framework)')
    pdf.table_row('Microcontroller', 'ESP32 DevKit')
    pdf.table_row('MQTT Broker', 'HiveMQ Cloud (Free Tier)')
    pdf.table_row('Protocol', 'MQTT over TLS (MQTTS)')
    pdf.table_row('IDE', 'VS Code + ESP-IDF Extension')
    pdf.table_row('Language', 'C')
    pdf.table_row('RTOS', 'FreeRTOS')

    # --- Features ---
    pdf.section_title('11. Features')
    pdf.bullet_point('Secure MQTT communication over TLS')
    pdf.bullet_point('Remote LED control from anywhere via internet')
    pdf.bullet_point('Auto Wi-Fi reconnection on disconnection')
    pdf.bullet_point('Clean event-driven architecture')
    pdf.bullet_point('HiveMQ Cloud free tier compatible')
    pdf.bullet_point('Minimal build configuration for fast compilation')
    pdf.bullet_point('Error handling with detailed ESP logging')

    # --- Conclusion ---
    pdf.section_title('12. Conclusion')
    pdf.body_text(
        'This project successfully demonstrates IoT-based remote control of a hardware '
        'peripheral (LED) using the MQTT protocol with cloud connectivity. The ESP32 securely '
        'connects to HiveMQ Cloud and responds to real-time commands, showcasing a practical '
        'IoT publish-subscribe pattern.'
    )
    pdf.body_text(
        'This architecture can be extended to control motors, relays, sensors, and other '
        'actuators, making it a solid foundation for more complex IoT applications such as '
        'smart home automation, industrial monitoring, and remote device management.'
    )

    # --- Save PDF ---
    output_path = os.path.join(script_dir, 'MQTT_LED_HiveMQ_Project_Report.pdf')
    pdf.output(output_path)
    print(f"PDF report generated successfully: {output_path}")


if __name__ == '__main__':
    generate_report()
